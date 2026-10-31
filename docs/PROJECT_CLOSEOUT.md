# Project close-out and development freeze

## Final scope

The fourteen backlog items P01–P14 are implemented. Each item has an assignee, estimate, requirement references, sprint assignment, and Done status on the GitHub Project board. P01–P03 and P05–P09 are grouped under Sprint 1; P04 and P10–P14 are grouped under Sprint 2, preserving the board's existing Sprint 2 assignment for fees. Issue #12 was closed after its implementation merged in PR #40.

Follow-up issue #44 completes the React workflows for fees and facilities that were missing from the first frozen snapshot. Students can view balances and record payments, browse facility availability, and book slots; staff can manage fee records and facility entries. The client intentionally records payments through the project API and does not connect to a payment gateway.

Follow-up issue #46 completes the shared visual system across the frontend, including profile and complaint surfaces, form feedback, responsive tables, navigation, focus states, and tablet/mobile layouts.

The Sprint 1 demo recording is committed as `Demo 1.mov`. Sprint 2's implementation and reports are present; the Sprint 2 demo video is a separate submission artifact and is not included in this code freeze.

## Verification evidence

- GitHub Actions runs Django configuration checks and the backend test suite against PostgreSQL for pull requests and pushes to `main`.
- The final feature PRs passed GitHub Actions. The local backend run completed 82 tests with one skipped, and `manage.py check` reported no issues.
- The production frontend build (`npm run build`) passes with the fees and facilities workflows included.
- The same production build validates the final responsive styling and component states.
- Sprint 2 evidence is recorded in `SPRINT_2_RESPONSE_TIME.md`, `SPRINT_2_AVAILABILITY_REPORT.md`, `SPRINT_2_USABILITY_REPORT.md`, and `../load_tests/README.md`.
- Implementation differences from the submitted design are recorded in `IMPLEMENTATION_DEVIATIONS.md`.

## Limits of the evidence

Performance and load results were collected with a local development server and SQLite; they do not establish production capacity. Availability sampling is preliminary, and the usability report is a self-walkthrough rather than an independent participant study. Keep these limitations attached to any presentation of the results.

The Sprint 1 retrospective records formal GitHub approval for PR #31. Other Sprint 1 reviews were documented retrospectively because the PRs had already merged.

## Freeze

The `v1.0.2` course-project release, published after issue #46 is merged and verified, supersedes the earlier `v1.0.0` and `v1.0.1` snapshots and defines the final baseline. Feature development is frozen at `v1.0.2`. Any later code change should start with a new issue and go through a reviewed pull request with passing CI; it should not be added directly to the frozen release.
