# Sprint 2 response-time task (#19)

**Target:** Standard requests complete within two seconds under normal load.

## TC-012 measurement profile

- Request: authenticated `GET /api/v1/complaints` with 100 representative complaint records.
- Normal load: 50 concurrent virtual users, each making one request every five seconds (about 10 requests per second).
- Warm-up: 60 seconds. Measurement window: 300 seconds.
- Threshold method: p95 latency <= 2,000 ms and failed requests < 1%.
- The runner reports p50, p95, p99, maximum latency, status counts, and failures.

## Reproduce locally

Use two PowerShell terminals from the repository root. This uses the local SQLite development database and refuses to seed a PostgreSQL database.

Terminal 1:

```powershell
python backend/manage.py migrate --noinput
python backend/manage.py runserver 127.0.0.1:8000 --noreload
```

Terminal 2:

```powershell
$env:HMS_BENCHMARK_TOKEN = python docs/prepare_sprint2_response_time.py
python docs/benchmark_sprint2_response_time.py
Remove-Item Env:HMS_BENCHMARK_TOKEN
```

## Execution record

- **Date:** 2026-10-30
- **Environment:** Local Django development server with SQLite; 100 seeded complaint records for the benchmark student.
- **Profile:** 50 virtual users, five-second think time, 60-second warm-up, 300-second measurement window.
- **Samples:** 2,999 requests; 0 failed (0%).
- **Latency:** p50 31 ms; p95 47 ms; p99 110 ms; maximum 375 ms.
- **Result:** **PASS** for this profile in the recorded local environment (p95 <= 2,000 ms; failures < 1%).

The measured result meets the target for this local setup. The Django development server and SQLite are not production infrastructure, so rerun the profile against the production-like environment before treating it as a release performance guarantee.
