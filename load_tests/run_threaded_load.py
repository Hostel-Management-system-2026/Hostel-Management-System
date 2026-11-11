"""Run the student read-workflow profile with only the Python standard library.

This is a reproducible fallback runner for hosts where Locust/gevent cannot be
installed. It preserves the same 500-user, 10-user/second, two-minute profile.
"""

import argparse
import concurrent.futures
import csv
import json
import random
import threading
import time
from datetime import datetime, timezone
from http.client import HTTPConnection, HTTPSConnection
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
DEFAULT_CREDENTIALS = ROOT / "data" / "students.csv"
WORKFLOW_PATHS = (
    "/api/v1/profiles/me",
    "/api/v1/profiles/me",
    "/api/v1/profiles/me",
    "/api/v1/profiles/me",
    "/api/v1/notices",
    "/api/v1/notices",
    "/api/v1/notices",
    "/api/v1/notices",
    "/api/v1/mess/menu",
    "/api/v1/mess/menu",
    "/api/v1/mess/menu",
    "/api/v1/mess/menu",
    "/api/v1/facilities/",
    "/api/v1/facilities/",
    "/api/v1/facilities/",
    "/api/v1/leave",
    "/api/v1/leave",
    "/api/v1/leave",
    "/api/v1/complaints",
    "/api/v1/complaints",
    "/api/v1/complaints",
)
CSV_FIELDS = (
    "timestamp_utc",
    "elapsed_seconds",
    "user_number",
    "method",
    "endpoint",
    "status_code",
    "latency_ms",
    "error",
)


def read_credentials(path, count):
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) < count:
        raise SystemExit(f"Need {count} credentials in {path}; found {len(rows)}.")
    return rows[:count]


def request(connection, method, path, body=None, headers=None):
    started = time.perf_counter()
    status = ""
    error = ""
    response_body = b""
    try:
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        status = response.status
        response_body = response.read()
        if not 200 <= status < 300:
            error = f"HTTP {status}"
    except Exception as exc:  # record network and protocol failures in the raw log
        error = type(exc).__name__
        try:
            connection.close()
        except Exception:
            pass
    return status, (time.perf_counter() - started) * 1000, error, response_body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--users", type=int, default=500)
    parser.add_argument("--spawn-rate", type=float, default=10)
    parser.add_argument("--run-time", type=float, default=120)
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.users < 1 or args.spawn_rate <= 0 or args.run_time <= 0:
        parser.error("users, spawn-rate, and run-time must be positive")

    credentials = read_credentials(args.credentials, args.users)
    host = urlparse(args.host)
    if host.scheme not in {"http", "https"} or not host.hostname:
        parser.error("host must be an http:// or https:// URL")
    port = host.port or (443 if host.scheme == "https" else 80)
    prefix = host.path.rstrip("/")
    connection_type = HTTPSConnection if host.scheme == "https" else HTTPConnection
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    started_utc = datetime.now(timezone.utc)
    start = time.monotonic()
    stop_at = start + args.run_time
    events = []
    events_lock = threading.Lock()
    authenticated = set()

    def record(user_number, method, endpoint, status, latency, error):
        event = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "user_number": user_number,
            "method": method,
            "endpoint": endpoint,
            "status_code": status,
            "latency_ms": round(latency, 3),
            "error": error,
        }
        with events_lock:
            events.append(event)

    def user_task(index, student, spawn_at):
        delay = spawn_at - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        conn = connection_type(host.hostname, port, timeout=20)
        try:
            body = json.dumps({
                "username": student["username"],
                "password": student["password"],
            })
            status, latency, error, response_body = request(
                conn,
                "POST",
                f"{prefix}/api/v1/auth/login/",
                body=body,
                headers={"Content-Type": "application/json"},
            )
            record(index, "POST", "/api/v1/auth/login/", status, latency, error)
            if status != 200:
                return
            try:
                token = json.loads(response_body)["access"]
            except (ValueError, KeyError, TypeError):
                record(index, "POST", "/api/v1/auth/login/", status, 0, "Missing access token")
                return
            authenticated.add(index)

            headers = {"Authorization": f"Bearer {token}"}
            route_index = index % len(WORKFLOW_PATHS)
            while time.monotonic() < stop_at:
                endpoint = WORKFLOW_PATHS[route_index]
                status, latency, error, _ = request(
                    conn, "GET", f"{prefix}{endpoint}", headers=headers
                )
                record(index, "GET", endpoint, status, latency, error)
                route_index = (route_index + 1) % len(WORKFLOW_PATHS)
                time.sleep(random.uniform(1, 3))
        finally:
            conn.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.users) as pool:
        futures = []
        for index, student in enumerate(credentials):
            futures.append(pool.submit(
                user_task,
                index + 1,
                student,
                start + index / args.spawn_rate,
            ))
        for future in concurrent.futures.as_completed(futures):
            future.result()

    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(sorted(events, key=lambda item: item["elapsed_seconds"]))

    api_events = [event for event in events if event["method"] == "GET"]
    latencies = sorted(event["latency_ms"] for event in api_events)
    failures = [event for event in events if event["error"]]

    def percentile(values, fraction):
        if not values:
            return None
        return values[min(len(values) - 1, int((len(values) - 1) * fraction))]

    summary = {
        "started_utc": started_utc.isoformat(),
        "host": args.host,
        "profile": {
            "virtual_users": args.users,
            "spawn_rate_users_per_second": args.spawn_rate,
            "run_time_seconds": args.run_time,
            "think_time_seconds": [1, 3],
            "runner": "Python standard library threaded HTTP runner",
        },
        "authenticated_users": len(authenticated),
        "total_requests": len(events),
        "read_requests": len(api_events),
        "failed_requests": len(failures),
        "failure_rate_percent": round(100 * len(failures) / len(events), 4) if events else None,
        "read_latency_ms": {
            "average": round(sum(latencies) / len(latencies), 3) if latencies else None,
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
            "maximum": max(latencies) if latencies else None,
        },
        "raw_csv": str(output),
    }
    summary_path = output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
