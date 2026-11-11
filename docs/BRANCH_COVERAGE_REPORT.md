# Branch coverage report

**Date:** 4 November 2026  
**Tool:** coverage.py 7.17.1, branch measurement enabled

## Result

| Metric | Result |
|---|---:|
| Application branch opportunities | 124 |
| Branches exercised | 84 |
| Missing branches | 40 |
| Partial branches | 26 |
| Branch coverage | 67.7% |

The report used the same SQLite 90-test execution as `CODE_COVERAGE_REPORT.md` (89 passed, one skipped). It excludes test files, migrations, admin/app/URL registration modules, Django config entry points, and the load-test account management command. Branch coverage is below statement coverage because some conditional/error paths were not exercised in this SQLite coverage run. The PostgreSQL-only concurrency case passed in the separate PostgreSQL 18 suite but is not represented in these SQLite coverage figures. See `coverage report -m --omit='*/tests.py,*/test_*.py,*/migrations/*,*/admin.py,*/apps.py,*/urls.py,*/config/*,*/management/*'` for per-file missing lines and branches.

This is measured test evidence, not a claim that every condition or deployment scenario has been validated. Highest-value follow-up is to run PostgreSQL CI for row-lock behavior and add explicit tests for uncovered profile update and authorization paths.
