"""Run the Sprint 2 #19 response-time profile against the HMS API."""

import argparse
import concurrent.futures
import json
import math
import os
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(fraction * len(ordered)) - 1)] if ordered else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--path", default="/api/v1/complaints")
    parser.add_argument("--token", default=os.environ.get("HMS_BENCHMARK_TOKEN"))
    parser.add_argument("--users", type=int, default=50)
    parser.add_argument("--warmup-seconds", type=int, default=60)
    parser.add_argument("--measure-seconds", type=int, default=300)
    parser.add_argument("--think-seconds", type=float, default=5.0)
    args = parser.parse_args()
    if not args.token:
        parser.error("pass --token or set HMS_BENCHMARK_TOKEN")
    if args.users < 1 or args.warmup_seconds < 0 or args.measure_seconds < 1 or args.think_seconds < 0:
        parser.error("users and measurement duration must be positive; warm-up and think time cannot be negative")

    start = time.monotonic()
    measure_at = start + args.warmup_seconds
    finish_at = measure_at + args.measure_seconds
    lock = threading.Lock()
    latencies = []
    failures = 0
    total = 0
    status_counts = {}
    url = args.base_url.rstrip("/") + args.path

    def worker():
        nonlocal failures, total
        while time.monotonic() < finish_at:
            request = urllib.request.Request(
                url,
                headers={"Authorization": f"Bearer {args.token}", "Accept": "application/json"},
            )
            request_started = time.monotonic()
            success = False
            status_code = None
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    response.read()
                    status_code = response.status
                    success = 200 <= response.status < 300
            except urllib.error.HTTPError as error:
                status_code = error.code
            except (urllib.error.URLError, TimeoutError, OSError):
                success = False
            elapsed_ms = (time.monotonic() - request_started) * 1000
            if request_started >= measure_at:
                with lock:
                    total += 1
                    key = str(status_code) if status_code is not None else "transport_error"
                    status_counts[key] = status_counts.get(key, 0) + 1
                    if success:
                        latencies.append(elapsed_ms)
                    else:
                        failures += 1
            time.sleep(args.think_seconds)

    started_at = datetime.now(timezone.utc).isoformat()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.users) as pool:
        futures = [pool.submit(worker) for _ in range(args.users)]
        for future in futures:
            future.result()

    failed_rate = failures / total if total else 1.0
    result = {
        "started_at_utc": started_at,
        "target": url,
        "normal_load_profile": {
            "virtual_users": args.users,
            "think_seconds": args.think_seconds,
            "warmup_seconds": args.warmup_seconds,
            "measurement_seconds": args.measure_seconds,
        },
        "threshold_method": "p95 <= 2000 ms; failed requests < 1%",
        "requests": total,
        "failed_requests": failures,
        "failed_rate_percent": round(failed_rate * 100, 3),
        "status_counts": status_counts,
        "latency_ms": {
            "p50": round(percentile(latencies, 0.50), 2) if latencies else None,
            "p95": round(percentile(latencies, 0.95), 2) if latencies else None,
            "p99": round(percentile(latencies, 0.99), 2) if latencies else None,
            "max": round(max(latencies), 2) if latencies else None,
        },
    }
    p95 = result["latency_ms"]["p95"]
    result["result"] = "PASS" if p95 is not None and p95 <= 2000 and failed_rate < 0.01 else "FAIL"
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
