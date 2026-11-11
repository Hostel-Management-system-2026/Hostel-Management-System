# System validation report

**Date:** 4 November 2026  
**Status:** Core API workflows validated; deployment-level targets remain limited by local test conditions

## Scope and environment

System validation used the Django REST API, configured permissions, serializers, business rules, and an isolated SQLite test database. The application-level test suite ran 90 cases: 89 passed and one PostgreSQL-specific concurrency case was skipped. The frontend production bundle also built successfully with `npm run build` (Vite 8.3.4, TypeScript project build).

Automated API scenarios cover login and JWT role enforcement, student-owned profile/fee/leave access, room allocation, partial and full fee settlement, complaint transitions, visitor entry and exit, weekly menu publication, notices, leave decisions, and facility availability/booking conflicts.

## Results

| Validation | Result | Evidence |
|---|---|---|
| Django configuration | Pass | `manage.py check`: no issues. |
| Backend API/business-rule suite | Pass with one skip | 90 tests; 89 passed; 1 PostgreSQL-only concurrency test skipped on SQLite. |
| Frontend production build | Pass | `npm run build`; TypeScript and Vite build succeeded. |
| Standard request latency | Local profile pass | p95 47 ms, 0 failures at 50 users; see `SPRINT_2_RESPONSE_TIME.md`. |
| 500-user load | Local profile pass | 500/500 synthetic accounts authenticated; 12,788 requests and zero failures. Raw per-request CSV and JSON summary are under `../load_tests/evidence/2026-11-10/`. |
| Availability | Pass by sample-count criterion | All 360 recorded checks succeeded (100%), above the 99% sampled target. Timestamp gaps are disclosed as context; elapsed time is not the acceptance condition. |
| Staff usability | Workable; ready for participant testing | Warden task workflows are present and a five-participant protocol is ready; participant results and the 90% target measurement are pending. |

## Limitations

- No browser automation suite is configured, so the React workflows were production-built but not automatically exercised through a browser in this run.
- SQLite validation does not prove PostgreSQL row-lock behavior. That case passed in the separately recorded full PostgreSQL 18 suite; it is skipped only when the suite runs on SQLite.
- Local development-server performance, load, and availability results are not production-capacity or service-level guarantees.
- The usability walkthrough was not an independent participant study.

Detailed planned-case outcomes are in `TEST_PLAN_EXECUTION_ADDENDUM.md`.

## Follow-up validation — 10 November 2026

- The backend suite passed all 90 tests on PostgreSQL 18. The SQLite run passed 89 tests with the expected PostgreSQL-only concurrency test skipped. Django checks passed on both databases.
- The frontend production build passed.
- The reproducible local 500-user profile authenticated 500/500 synthetic accounts and completed 12,788 requests with zero failures. Raw per-request CSV and summary JSON are stored under `../load_tests/evidence/2026-11-10/`. The run used SQLite, Django's development server, and a test-only PBKDF2 work factor for disposable accounts, so it is not production-capacity evidence.
- Availability sample collection reached 360 successful checks with zero failures (100%). Raw timestamps contain a 54,714-second gap and a 109-second gap; TC-014 is complete by sample-count/success-rate criterion, while these gaps remain a limitation on continuous-uptime interpretation. Raw samples and summary are in `../load_tests/evidence/2026-11-10/`.
- TC-015 is ready for independent staff testing. The prior self-walkthrough is not counted; the protocol is `STAFF_USABILITY_PROTOCOL.md`, and the participant results remain pending.

## Final local verification — 11 November 2026

- `python manage.py check`: no issues.
- `python manage.py test` on SQLite: 90 tests run, 89 passed, and the PostgreSQL-only row-lock concurrency test was skipped; suite passed in 348.8 seconds.
- `npm.cmd run build`: TypeScript and Vite production build passed.
- The SQLite skip is covered by the previously recorded PostgreSQL 18 suite, which passed all 90 tests.
