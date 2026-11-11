# Hostel Management System – Load Testing

## 1. Objective

The objective of this load-testing setup is to evaluate the performance of the Hostel Management System backend under concurrent student activity, with a target of 500 concurrent student users.

Locust is used to simulate student activity and measure API response times, throughput, and request failures.

## 2. Technology Stack

- Python
- Django REST Framework
- Locust
- SQLite (local testing configuration)

## 3. Student Workflows Tested

The load test covers the following seven workflows:

1. Student authentication
2. View student profile
3. View notices
4. View mess menu
5. View facilities
6. View leave requests
7. View complaints

Each virtual student uses a separate synthetic account and JWT authentication.

## 4. Test Account Generation

From the backend directory, execute:

```bash
python manage.py create_load_test_students --count 500 --confirm
```

This creates up to 500 synthetic student accounts and stores their credentials in:

`load_tests/data/students.csv`

Never commit this credentials file.

## 5. Installing Dependencies

From the repository root:

```bash
pip install -r load_tests/requirements.txt
```

## 6. Running the Load Test

Start the Django development server from the backend directory:

```bash
python manage.py runserver
```

From the repository root, execute Locust:

```bash
locust -f load_tests/locustfile.py --host http://127.0.0.1:8000 --users 500 --spawn-rate 10 --run-time 2m --headless --csv load_tests/results/test_500_users
```

## 7. Test Results

| Concurrent Users | Total Requests | Failed Requests | Average Response Time | Throughput |
|---:|---:|---:|---:|---:|
| 10 | 595 | 0 | 8 ms | 4.99 req/s |
| 50 | 2,935 | 0 | 7 ms | 24.52 req/s |
| 100 | 5,855 | 0 | 8 ms | 48.86 req/s |
| 250 | 13,808 | 0 | 7 ms | 115.32 req/s |
| 500 | 24,366 | 0 | 7 ms | 203.47 req/s |

### 500-user test details

- Concurrent users: 500
- Total requests: 24,366
- Failed requests: 0
- Failure rate: 0%
- Average response time: 7 ms
- Median response time: 2 ms
- 95th percentile response time: 10 ms
- Maximum response time: 243 ms
- Throughput: 203.47 requests/second

All seven tested workflows completed without reported request failures.

## 8. Test Environment and Limitations

The tests were conducted locally using the Django development server and SQLite, with Locust running on the same MacBook.

The 500-user test used a spawn rate of 10 users per second and a total runtime of two minutes. The ramp-up to 500 users took approximately 50 seconds, so the full 500-user load was maintained for approximately 70 seconds.

These results demonstrate the behavior of the local test setup. They do not establish production capacity.

Formal production-capacity validation should use PostgreSQL, deployment-like infrastructure, and preferably a separate load-generation machine.

## 9. Security Considerations

- Use synthetic student accounts only.
- Never commit generated passwords.
- Keep `students.csv` excluded through `.gitignore`.
- Do not run load tests against production without authorization.
- Generated CSV and HTML reports are excluded from Git.

## 10. Conclusion

The local load-testing setup successfully completed a test with 500 simulated concurrent student users and reported zero failed requests across 24,366 requests.

Further deployment-like testing is required before making production-capacity claims.

## Reproducible execution — 10 November 2026

The current Windows/Python 3.14 environment could not build Locust's `gevent` dependency, so this run used `run_threaded_load.py`, a standard-library HTTP runner with the same 500 users, 10 users/second ramp, two-minute duration, 1–3 second think time, login, and six read workflows. It writes per-request timestamps, status, latency, and errors to CSV and a machine-readable summary JSON.

Run from the repository root. These settings and accounts are only for local synthetic testing; the low PBKDF2 work factor is not suitable for real accounts or deployment.

```powershell
$env:DJANGO_SETTINGS_MODULE = 'config.load_test_settings'
python backend/manage.py migrate --noinput
python backend/manage.py create_load_test_students --count 500 --confirm
python load_tests/prepare_test_data.py
```

In a second terminal, from the repository root:

```powershell
$env:DJANGO_SETTINGS_MODULE = 'config.load_test_settings'
python load_tests/run_dev_server.py 127.0.0.1:8000 --noreload --verbosity 0
```

In a third terminal:

```powershell
python load_tests/run_threaded_load.py `
  --host http://127.0.0.1:8000 `
  --users 500 `
  --spawn-rate 10 `
  --run-time 120 `
  --output load_tests/evidence/2026-11-10/500_user_requests.csv
```

After both the load run and any availability observation finish, remove the synthetic users, their dependent profiles, the matching synthetic menu, and the ignored credential file:

```powershell
python load_tests/cleanup_test_data.py
```

### Run result

| Metric | Result |
|---|---:|
| Accounts authenticated | 500 / 500 |
| Total requests (login + reads) | 12,788 |
| Read requests | 12,288 |
| Failed requests | 0 |
| Read latency p50 / p95 / p99 | 2,089.7 / 3,818.2 / 5,737.2 ms |
| Maximum read latency | 8,572.5 ms |
| Overall throughput during the 120-second profile | 106.6 requests/second |

Raw data stored in the local working tree: [`500_user_requests.csv`](evidence/2026-11-10/500_user_requests.csv) and [`500_user_requests.summary.json`](evidence/2026-11-10/500_user_requests.summary.json). The two failed diagnostic attempts are retained in the same evidence folder and are not counted as the final run.

The profile ran against SQLite and Django's local development server on the same Windows machine. The test-specific settings used PBKDF2 with 1,000 iterations for disposable synthetic accounts and the load server used a larger connection backlog. These results are repeatable local evidence, not a production-capacity or real-password-hashing result.

## Availability observation

With the local server running and synthetic credentials available, run a one-hour, ten-second-interval authenticated API observation as follows:

```powershell
python load_tests/monitor_availability.py `
  --host http://127.0.0.1:8000 `
  --duration-seconds 3600 `
  --interval-seconds 10 `
  --refresh-seconds 240 `
  --output load_tests/evidence/2026-11-10/availability_1h.csv
```

The monitor refreshes its JWT during the run and writes each sample immediately to CSV. It also writes a summary JSON after the final check. This is a local development-server observation, not a production uptime guarantee.

`--resume` appends checks until the requested total row count is reached; it does not replace time lost during an interruption. The summary records the wall-clock span, largest sample gap, and whether the samples meet a continuous-observation check (no gap over 1.5 times the interval). For a one-hour continuity target, start a fresh CSV and keep the monitor running without interruption. Treat resumed samples with excessive gaps as partial evidence.
