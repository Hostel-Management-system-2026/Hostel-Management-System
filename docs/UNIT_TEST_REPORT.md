# Unit and API test report

**Date:** 4 November 2026  
**Status:** Pass with one environment-specific skip

## Execution

The Django automated test suite was run against its isolated SQLite test database using Python 3.12 and Django 5.2.19.

```powershell
..\.venv-win\Scripts\python.exe manage.py check
..\.venv-win\Scripts\python.exe -m coverage run --branch --source=accounts,complaints,facilities,fees,leave_requests,mess,notices,profiles,room_allocations,visitors,common,config manage.py test
```

## Result

- 90 tests run.
- 89 passed; 1 skipped.
- Runtime: 416.4 seconds.
- Django system check: no issues.

The suite contains Django `TestCase`, `APITestCase`, and one `TransactionTestCase` group. It covers authentication and role checks, profiles, allocations, fees, complaints, visitors, mess, leave, notices, and facility workflows. Since most cases exercise REST endpoints and persistence together, the suite is best understood as unit plus API/component integration evidence, not as an isolated pure-unit suite.

The skipped case in this SQLite coverage run is the PostgreSQL-specific concurrent room-capacity test. It passed in the separately recorded full PostgreSQL 18 suite. Additional cases added for this closeout cover profile read-only enforcement and Admin updates, notice CRUD permissions, room inventory and allocation release, and visitor filtering/server-time exit behavior.

See `TEST_PLAN_EXECUTION_ADDENDUM.md` for traceability to the 15 planned cases and `SYSTEM_VALIDATION_REPORT.md` for end-to-end scope and limits.
