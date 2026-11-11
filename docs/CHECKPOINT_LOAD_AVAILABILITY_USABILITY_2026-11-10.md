# Load, availability, and usability checkpoint

**Checkpoint date:** 10 November 2026; resumed 11 November 2026  
**Status:** TC-014 complete by the 360-check sampled-success criterion. No application server or test process is running.

All evidence and code changes listed here are local working-tree files; nothing was committed or pushed. Existing uncommitted changes were preserved.

## Completed: 500-user load run

- 500/500 synthetic student accounts authenticated.
- 12,788 requests total: 500 logins and 12,288 authenticated reads across profile, notices, mess menu, facilities, leave, and complaints.
- Zero failed requests.
- Read latency: p50 2,089.7 ms; p95 3,818.2 ms; p99 5,737.2 ms; maximum 8,572.5 ms.
- Profile: 10 users/second spawn rate, 120 seconds, 1–3 second think time.
- Raw evidence: [`500_user_requests.csv`](../load_tests/evidence/2026-11-10/500_user_requests.csv) and [`500_user_requests.summary.json`](../load_tests/evidence/2026-11-10/500_user_requests.summary.json).
- Two unsuccessful diagnostic attempts are retained under `../load_tests/evidence/2026-11-10/attempt-1-default-backlog/` and `attempt-2-default-hasher/`. They are excluded from the successful result.

The run used the standard-library threaded runner because Locust's `gevent` dependency could not be built in the installed Python 3.14 environment. It used local SQLite and Django's development server on the same machine. Disposable accounts used a test-only PBKDF2 work factor of 1,000 iterations and the test server used an enlarged request backlog. The measured result is local test evidence, not production-capacity or production password-hashing evidence.

Reproduction instructions and configuration are in [`load_tests/README.md`](../load_tests/README.md). The synthetic account generator and test-only settings are `backend/accounts/management/commands/create_load_test_students.py` and `backend/config/load_test_settings.py`.

## Completed: availability sample criterion

- Target: 360 authenticated checks with JWT refresh every 240 seconds.
- Result: **360/360 checks succeeded; zero failures (100%)**, exceeding the 99% sampled target.
- The CSV spans 58,392.8 wall-clock seconds and contains two gaps over 15 seconds; the largest gap is 54,714.0 seconds. It therefore does not satisfy a continuous one-hour observation.
- Endpoint latency average / maximum: **19.558 / 264.221 ms**.
- Raw samples: [`availability_1h.csv`](../load_tests/evidence/2026-11-10/availability_1h.csv).
- Final summary: [`availability_1h.summary.json`](../load_tests/evidence/2026-11-10/availability_1h.summary.json).

TC-014 is complete by the sampled success-rate criterion. The timestamp gaps are retained as context and mean the sample does not measure continuous uptime. This local test is not a production SLA.
## Ready for independent staff usability testing

The Warden workflows and the ready-to-use task protocol and anonymized score sheet are in [`STAFF_USABILITY_PROTOCOL.md`](STAFF_USABILITY_PROTOCOL.md). The earlier self-walkthrough is not counted as independent evidence. Five real staff participants need to complete the eight tasks; at least 36 of 40 task attempts must succeed to meet the 90% target. The work is ready to run, with participant results pending.

## Test data cleanup

After sample collection stopped, `load_tests/cleanup_test_data.py` removed 500 synthetic accounts, the matching synthetic weekly menu, and the ignored `load_tests/data/students.csv` credentials file. The raw availability evidence and summary remain in the repository working tree.

## Other verification already completed

Earlier in this session, the backend suite passed all 90 tests on PostgreSQL 18; SQLite passed 89 with the PostgreSQL-only concurrency test skipped. Django checks and the frontend production build passed. Those results are recorded in `TEST_PLAN_EXECUTION_ADDENDUM.md`.
