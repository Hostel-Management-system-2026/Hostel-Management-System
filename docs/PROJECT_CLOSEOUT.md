# Project close-out and development freeze

## Final scope

The fourteen backlog items P01–P14 are implemented. Each item has an assignee, estimate, requirement references, sprint assignment, and Done status on the GitHub Project board. P01–P03 and P05–P09 are grouped under Sprint 1; P04 and P10–P14 are grouped under Sprint 2, preserving the board's existing Sprint 2 assignment for fees. Issue #12 was closed after its implementation merged in PR #40.

Follow-up issue #44 completes the React workflows for fees and facilities that were missing from the first frozen snapshot. Students can view balances and record payments, browse facility availability, and book slots; staff can manage fee records and facility entries. The client intentionally records payments through the project API and does not connect to a payment gateway.

Follow-up issue #46 completes the shared visual system across the frontend, including profile and complaint surfaces, form feedback, responsive tables, navigation, focus states, and tablet/mobile layouts.

The Sprint 1 and Sprint 2 demo recordings are committed as `Demo 1.mov` and `Demo 2.mov`.

## Verification evidence

- GitHub Actions runs Django configuration checks and the backend test suite against PostgreSQL for pull requests and pushes to `main`.
- The final feature PRs passed GitHub Actions. The local backend run completed 82 tests with one skipped, and `manage.py check` reported no issues.
- The production frontend build (`npm run build`) passes with the fees and facilities workflows included.
- On 4 November 2026, the local Django system check passed and the backend suite ran 90 tests: 89 passed and one PostgreSQL-only concurrency test was skipped on SQLite.
- On 4 November 2026, the frontend production build (`npm run build`) passed with TypeScript and Vite.
- The coverage run measured 93.1% application statement coverage and 67.7% application branch coverage; see `CODE_COVERAGE_REPORT.md` and `BRANCH_COVERAGE_REPORT.md`.
- Sprint 2 evidence is recorded in `SPRINT_2_RESPONSE_TIME.md`, `SPRINT_2_AVAILABILITY_REPORT.md`, `SPRINT_2_USABILITY_REPORT.md`, and `../load_tests/README.md`. Current planned-case statuses are summarized in `TEST_PLAN_EXECUTION_ADDENDUM.md`.
- `DESIGN_API_AND_SEQUENCE_ADDENDUM.md` supplies two implementation-aligned sequence diagrams, endpoint design, error handling, and traceability alongside the architecture PDF.
- Unit/API and system validation records are in `UNIT_TEST_REPORT.md` and `SYSTEM_VALIDATION_REPORT.md`.
- Implementation differences from the submitted design are recorded in `IMPLEMENTATION_DEVIATIONS.md`.

## Limits of the evidence

Performance, load, and availability results were collected with a local development server and SQLite; they do not establish production capacity or a production availability SLA. All 360 recorded availability checks succeeded, meeting TC-014's sampled success-rate criterion; long timestamp gaps limit interpretation as continuous uptime. The usability report is a self-walkthrough rather than an independent participant study. Keep these limitations attached to any presentation of the results.

The SQLite backend run skips the PostgreSQL row-lock concurrency test; the PostgreSQL suite has run that test. The reproducible 500-user local profile has per-request CSV and JSON summary evidence under `load_tests/evidence/2026-11-10/`; it used the standard-library threaded runner because Locust could not be installed in the available Python environment. Branch coverage is 67.7%, so additional tests are needed before claiming comprehensive condition coverage.

The Sprint 1 retrospective records formal GitHub approval for PR #31. Other Sprint 1 reviews were documented retrospectively because the PRs had already merged.

## Freeze

The `v1.0.2` course-project release, published after issue #46 is merged and verified, supersedes the earlier `v1.0.0` and `v1.0.1` snapshots and defines the final baseline. Feature development is frozen at `v1.0.2`. Any later code change should start with a new issue and go through a reviewed pull request with passing CI; it should not be added directly to the frozen release.
