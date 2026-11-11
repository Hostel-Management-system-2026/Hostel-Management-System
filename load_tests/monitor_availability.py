"""Sample an authenticated API endpoint on a fixed schedule and log every check."""

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from http.client import HTTPConnection, HTTPSConnection
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
DEFAULT_CREDENTIALS = ROOT / "data" / "students.csv"
FIELDS = (
    "timestamp_utc",
    "elapsed_seconds",
    "endpoint_status",
    "endpoint_latency_ms",
    "refresh_status",
    "refresh_latency_ms",
    "success",
    "error",
)


def request_json(connection_type, host, port, path, payload=None, token=None):
    connection = connection_type(host, port, timeout=15)
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    started = time.perf_counter()
    try:
        connection.request("POST" if payload is not None else "GET", path, body, headers)
        response = connection.getresponse()
        raw = response.read()
        try:
            data = json.loads(raw) if raw else {}
        except ValueError:
            data = {}
        error = "" if 200 <= response.status < 300 else f"HTTP {response.status}"
        return response.status, (time.perf_counter() - started) * 1000, data, error
    except Exception as exc:
        return "", (time.perf_counter() - started) * 1000, {}, type(exc).__name__
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--duration-seconds", type=int, default=3600)
    parser.add_argument("--interval-seconds", type=int, default=10)
    parser.add_argument("--refresh-seconds", type=int, default=240)
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Append checks to an existing CSV until the target count is reached. "
            "Timestamp gaps remain and can invalidate a continuous observation."
        ),
    )
    args = parser.parse_args()
    if min(args.duration_seconds, args.interval_seconds, args.refresh_seconds) < 1:
        parser.error("duration, interval, and refresh must be positive")

    with args.credentials.open(newline="", encoding="utf-8") as stream:
        credentials = next(csv.DictReader(stream), None)
    if not credentials:
        raise SystemExit(f"No credentials found in {args.credentials}")

    parsed = urlparse(args.host)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        parser.error("host must be an http:// or https:// URL")
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    prefix = parsed.path.rstrip("/")
    connection_type = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
    login_path = f"{prefix}/api/v1/auth/login/"
    status, _, tokens, error = request_json(
        connection_type,
        host,
        port,
        login_path,
        {"username": credentials["username"], "password": credentials["password"]},
    )
    if status != 200 or not tokens.get("access") or not tokens.get("refresh"):
        raise SystemExit(f"Initial authentication failed: {error or status}")

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    previous_rows = []
    if args.resume:
        if not output.exists():
            parser.error("--resume requires an existing partial CSV")
        with output.open(newline="", encoding="utf-8") as stream:
            previous_rows = list(csv.DictReader(stream))
        if not previous_rows:
            parser.error("cannot resume an empty CSV")
        for row in previous_rows:
            row["success"] = row["success"].strip().lower() == "true"
            row["elapsed_seconds"] = float(row["elapsed_seconds"])
            row["endpoint_latency_ms"] = float(row["endpoint_latency_ms"])
    total = (args.duration_seconds + args.interval_seconds - 1) // args.interval_seconds
    if len(previous_rows) >= total:
        parser.error("the existing CSV already meets the requested duration")

    start_utc = (
        datetime.fromisoformat(previous_rows[0]["timestamp_utc"])
        if previous_rows
        else datetime.now(timezone.utc)
    )
    start = time.monotonic()
    elapsed_offset = (
        float(previous_rows[-1]["elapsed_seconds"]) + args.interval_seconds
        if previous_rows
        else 0.0
    )
    access = tokens["access"]
    refresh = tokens["refresh"]
    last_refresh = start
    checks = list(previous_rows)

    with output.open("a" if args.resume else "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if not args.resume:
            writer.writeheader()
        for number in range(len(previous_rows), total):
            scheduled = start + (number - len(previous_rows)) * args.interval_seconds
            delay = scheduled - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            timestamp = datetime.now(timezone.utc).isoformat()
            refresh_status = ""
            refresh_latency = ""
            errors = []

            if time.monotonic() - last_refresh >= args.refresh_seconds:
                refresh_status, refresh_latency, refreshed, refresh_error = request_json(
                    connection_type,
                    host,
                    port,
                    f"{prefix}/api/v1/auth/refresh/",
                    {"refresh": refresh},
                )
                if refresh_status == 200 and refreshed.get("access"):
                    access = refreshed["access"]
                    refresh = refreshed.get("refresh", refresh)
                    last_refresh = time.monotonic()
                else:
                    errors.append(f"refresh:{refresh_error or 'missing access token'}")

            endpoint_status, endpoint_latency, _, endpoint_error = request_json(
                connection_type,
                host,
                port,
                f"{prefix}/api/v1/complaints",
                token=access,
            )
            if endpoint_error:
                errors.append(f"endpoint:{endpoint_error}")
            success = endpoint_status in (200, 201, 204) and not errors
            row = {
                "timestamp_utc": timestamp,
                "elapsed_seconds": round(elapsed_offset + time.monotonic() - start, 3),
                "endpoint_status": endpoint_status,
                "endpoint_latency_ms": round(endpoint_latency, 3),
                "refresh_status": refresh_status,
                "refresh_latency_ms": round(refresh_latency, 3) if refresh_latency != "" else "",
                "success": success,
                "error": ";".join(errors),
            }
            writer.writerow(row)
            stream.flush()
            checks.append(row)

    successes = sum(row["success"] for row in checks)
    latencies = sorted(row["endpoint_latency_ms"] for row in checks)
    sample_times = [
        datetime.fromisoformat(row["timestamp_utc"])
        for row in checks
    ]
    sample_gaps = [
        (later - earlier).total_seconds()
        for earlier, later in zip(sample_times, sample_times[1:])
    ]
    gap_tolerance_seconds = args.interval_seconds * 1.5
    excessive_gaps = [
        gap for gap in sample_gaps if gap > gap_tolerance_seconds
    ]
    summary = {
        "started_utc": start_utc.isoformat(),
        "ended_utc": datetime.now(timezone.utc).isoformat(),
        "host": args.host,
        "endpoint": "/api/v1/complaints",
        "duration_seconds": args.duration_seconds,
        "duration_basis": "requested target; check count does not prove continuity",
        "interval_seconds": args.interval_seconds,
        "checks": len(checks),
        "successful_checks": successes,
        "failed_checks": len(checks) - successes,
        "success_rate_percent": round(100 * successes / len(checks), 4) if checks else None,
        "observed_wall_clock_span_seconds": (
            round((sample_times[-1] - sample_times[0]).total_seconds(), 3)
            if len(sample_times) > 1
            else 0
        ),
        "sample_gap_tolerance_seconds": gap_tolerance_seconds,
        "sample_gaps_over_tolerance": len(excessive_gaps),
        "largest_sample_gap_seconds": round(max(sample_gaps), 3) if sample_gaps else 0,
        "continuous_observation": not excessive_gaps and len(checks) == total,
        "endpoint_latency_ms": {
            "average": round(sum(latencies) / len(latencies), 3) if latencies else None,
            "maximum": max(latencies) if latencies else None,
        },
        "raw_csv": str(output),
    }
    summary_path = output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if successes != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
