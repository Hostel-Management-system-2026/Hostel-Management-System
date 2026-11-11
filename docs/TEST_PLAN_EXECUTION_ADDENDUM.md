# Test plan execution addendum

**Baseline:** `Test_Plan_Hostel_Management_System.pdf`, Version 1.1  
**Execution date:** 4 November 2026  
**Purpose:** Record available execution evidence against the PDF's 15 planned cases. This addendum supersedes the PDF's planning-only statement that all cases remain unexecuted. It does not change the requirements or claim that preliminary/local evidence proves production acceptance.

## Automated execution summary

- Command: `python manage.py check` and `python -m coverage run --branch --source=accounts,complaints,facilities,fees,leave_requests,mess,notices,profiles,room_allocations,visitors,common,config manage.py test`
- Environment: Python 3.12, Django 5.2.19, SQLite test database on Windows.
- Result: **90 tests run; 89 passed; 1 skipped** in 416.4 seconds. Django reported no configuration issues.
- Skip: PostgreSQL-specific concurrent room-capacity test; SQLite does not provide the row-lock behavior that test is designed to validate.
- The test suite exercises REST/API behavior and persistence through Django's test database. It is not a browser-based end-to-end suite.

## Planned test case status

| Test plan case | Result | Evidence / limitation |
|---|---|---|
| TC-001 Authenticate Admin, Warden, Student | **Pass** | Automated role login, invalid-password, password-hash, and token tests. |
| TC-002 Enforce role-based access | **Pass** | Automated permission tests cover Student, Warden, and Admin access across protected APIs. |
| TC-003 Allocate room; prevent multiple active allocations | **Pass** | Automated allocation, duplicate-active-allocation, capacity, unavailable-room, and authorization tests pass. Concurrent database locking is separately skipped on SQLite. |
| TC-004 Admin profile maintenance; Student read-only access | **Pass** | Automated tests cover Admin list/create/read/PUT/PATCH/delete and Student self-read plus denied PUT/PATCH/delete attempts. |
| TC-005 Partial/full fee payments and Paid-at-zero rule | **Pass** | Automated partial payment, full settlement, overpayment, ownership, and staff permission tests pass. |
| TC-006 Complaint status sequence | **Pass** | Automated creation, ownership/status protection, Warden transition, and invalid-skip tests pass. |
| TC-007 Visitor entry/exit timestamps | **Pass** | Automated required-entry, timestamp validation, role access, and single-exit tests pass. |
| TC-008 Publish/view weekly menu | **Pass** | Automated publishing, role access, replacement, validation, and current-menu selection tests pass. |
| TC-009 Leave request and Warden decision | **Pass** | Automated ownership, pending state, Warden decision, invalid date, and duplicate-decision tests pass. |
| TC-010 Admin notice to intended students | **Pass** | Automated publication, audience visibility, and role access tests pass. |
| TC-011 Facility booking and conflict rejection | **Pass** | Automated availability, successful booking, overlap rejection, adjacent slots, and role access tests pass. |
| TC-012 Standard response time under normal load | **Pass for recorded local profile** | `SPRINT_2_RESPONSE_TIME.md` records p95 47 ms and 0% failures for 50 users against local SQLite. Not a production-capacity claim. |
| TC-013 500 concurrent users | **Pass for the recorded local profile** | 500/500 synthetic accounts authenticated; 12,788 requests and zero failures. Raw per-request CSV and summary JSON are under `../load_tests/evidence/2026-11-10/`. The run used SQLite, the Django development server, and test-only password hashing, so it is not production-capacity evidence. |
| TC-014 Availability target | **Pass; complete by sample-count criterion** | All 360 recorded checks succeeded (100%), above the 99% target. Timestamp gaps are disclosed as context; elapsed time is not used as the acceptance condition. See `SPRINT_2_AVAILABILITY_REPORT.md`. |
| TC-015 Staff usability target | **Workable; ready for participant testing, results pending** | The source-level task-support review confirms the protocol's workflows are present. Independent staff sessions are still needed to measure the 90% completion target. |

## Remaining validation conditions

The room-capacity concurrency test has now run as part of the full PostgreSQL 18 suite above. Remaining evidence conditions are:

1. Repeat the 500-user profile on deployment-like infrastructure before making production-capacity claims; the local threaded-run raw evidence is already preserved.
2. TC-014 is complete by its 360-check sampled success-rate criterion. Production availability still requires deployment-like monitoring.
3. Conduct usability testing with representative staff participants and report the defined task-completion calculation.

Coverage figures are reported separately in `CODE_COVERAGE_REPORT.md` and `BRANCH_COVERAGE_REPORT.md`.

## Follow-up execution — 10 November 2026

The full Django suite and system check were rerun with Django 5.2.19 in the repository virtual environment (Python 3.14.10):

| Database | Result | Duration | Notes |
|---|---|---:|---|
| SQLite | **90 tests; 89 passed, 1 skipped** | 218.8 seconds | The PostgreSQL row-lock concurrency test is skipped because SQLite does not support the required row lock. |
| PostgreSQL 18 | **90 tests passed, none skipped** | 253.8 seconds | Ran against a temporary isolated cluster. The row-lock concurrency test ran as part of the full suite. The existing PostgreSQL service and database were not used. |

`manage.py check` reported no issues on both runs. The PostgreSQL run emitted PyJWT warnings because the temporary `HMS_SECRET_KEY` supplied for this local verification was shorter than the recommended 32 bytes; these were warnings, and all tests passed. The temporary database cluster was stopped and removed after the run.

## TC-013/TC-014 follow-up — 10 November 2026

- **TC-013:** A reproducible 500-account local profile completed with 500/500 successful authentications, 12,788 total requests (12,288 reads), and zero failures. The standard-library threaded runner and raw per-request CSV are in `../load_tests/README.md` and `../load_tests/evidence/2026-11-10/`. The local profile used SQLite, the Django development server, and test-only PBKDF2 settings for synthetic accounts; it is not production-capacity evidence.
- **TC-014:** The CSV contains 360 successful checks and zero failures (100%), meeting the sampled 99% criterion. Timestamp analysis found a 54,714-second gap and a 109-second gap; these are disclosed as context and do not change the sample-count/success-rate result. See `SPRINT_2_AVAILABILITY_REPORT.md` and the raw CSV/summary in `../load_tests/evidence/2026-11-10/`.
- **TC-015:** The protocol and anonymized score sheet are ready in `STAFF_USABILITY_PROTOCOL.md`. The self-walkthrough and 11 November source review do not count as participant evidence; recruit five independent staff participants to measure the completion target.

## Final local verification — 11 November 2026

- Environment: Python 3.12.3, Django 5.2.19, SQLite.
- `manage.py check`: no issues.
- `manage.py test`: 90 tests run; 89 passed and the PostgreSQL-only row-lock test was skipped; suite passed in 348.8 seconds. The skipped case passed in the previously recorded PostgreSQL 18 suite.
- `npm.cmd run build`: TypeScript and Vite production build passed.
