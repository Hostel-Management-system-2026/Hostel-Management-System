# Code coverage report

**Date:** 4 November 2026  
**Tool:** coverage.py 7.17.1  
**Command:** `python -m coverage run --branch --source=accounts,complaints,facilities,fees,leave_requests,mess,notices,profiles,room_allocations,visitors,common,config manage.py test`

## Result

| Metric | Result |
|---|---:|
| Tests run | 90 |
| Passed / skipped | 89 / 1 |
| Executable statements in application modules | 827 |
| Statements covered in application modules | 770 |
| Statement coverage in application modules | 93.1% |
| Combined coverage.py total (statements + branches, same scope) | 89.8% |

The application-module scope excludes test files, migrations, admin/app/URL registration modules, Django config entry points, and the load-test account management command. Reproduce the scoped report with `python -m coverage report --omit='*/tests.py,*/test_*.py,*/migrations/*,*/admin.py,*/apps.py,*/urls.py,*/config/*,*/management/*'`. Per-file results are produced by `coverage report -m`; branch totals are in `BRANCH_COVERAGE_REPORT.md`.

Coverage describes which Python lines the automated test run reached. It does not prove correctness of uncovered paths or replace PostgreSQL, browser, performance, availability, and usability validation. The skipped concurrency test is not covered by this SQLite run.

To reproduce, install `coverage` in the Python environment, run the command above from `backend/`, then run `python -m coverage report -m`.
