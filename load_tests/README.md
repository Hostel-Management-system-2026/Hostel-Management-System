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