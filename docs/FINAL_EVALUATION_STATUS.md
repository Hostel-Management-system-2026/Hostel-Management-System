# Final evaluation checklist status

**Review date:** 11 November 2026  
**Scope:** Checklist and FAQ tasks from the evaluator PDFs; deadlines excluded.

## Follow-up verification — 10–11 November 2026

- Re-read `FOR-EVALUATORS-TheCheckList.pdf` and `FOR-STUDENTS-FAQs_MiniProjectDemo.pdf`. The SRS, test plan, SAD, two design sequence diagrams, and four required `docs/` reports are present.
- `npm.cmd run build` completed successfully on 10 November 2026.
- The backend suite and Django system check were rerun on 10 November 2026. All 90 tests passed on PostgreSQL 18; 89 passed and the PostgreSQL-only row-lock test was skipped on SQLite. See `TEST_PLAN_EXECUTION_ADDENDUM.md` for durations and environment details.
- `manage.py check` reported no issues on both database runs. The frontend production build passed.
- The Sprint 2 recording is 157.03 seconds (2:37), longer than the checklist's 2-minute deliverable.
- Final local verification on 11 November: Django check passed; SQLite ran 90 tests (89 passed, 1 PostgreSQL-specific skip); and the frontend production build passed. The concurrency test passed in the recorded PostgreSQL 18 suite.

## Part 1 — Requirements and design

| Item | Status | Evidence |
|---|---|---|
| SRS structure, functional/non-functional requirements, use case diagram, security objectives and requirements | **Done** | `SRS/Member1_SRS_Hostel_Management_System.pdf` includes these sections and cites ISO/IEC/IEEE 29148:2018. |
| Test plan sections, security validation, traceability, and 7–10+ test cases | **Done** | `../Test_Plan_Hostel_Management_System.pdf` contains a dedicated security validation section, traceability, and 15 cases. Execution status is updated by `TEST_PLAN_EXECUTION_ADDENDUM.md`. |
| SAD architecture, components, traceability, security architecture | **Done** | `Architecture/Software_Architecture_Design_Specification.pdf`. |
| Two sequence diagrams, API design, and error handling | **Done** | `DESIGN_API_AND_SEQUENCE_ADDENDUM.md` adds two sequence diagrams, endpoint contracts, response conventions, and error handling aligned to the implementation. |

## Part 2 — Agile planning, repository, and sprints

| Item | Status | Evidence |
|---|---|---|
| GitHub backlog and project board, assignments, estimates, Sprint 1/2 planning | **Reported done; board not independently verified in this review** | `PROJECT_CLOSEOUT.md` records P01–P14 as assigned, estimated, and complete. The connected GitHub access exposed issue/PR operations but no project-board inspection capability. Issues #12, #44, and #46 were verified closed. |
| GitHub Actions | **Workflows present; latest remote run status unverified** | `.github/workflows/backend-tests.yml` and `frontend-build.yml` run on PRs and pushes to `main`. The linked GitHub status check returned no statuses for HEAD; local backend checks/tests and frontend build passed on 10 November. |
| Assigned-member PRs, formal owner reviews, and merges | **Partial; historical review evidence is missing** | GitHub review records were found for PRs #1, #4, and #31; PRs #23–#30 are explicitly documented as retrospective reviews, and the inspected later merged PRs have no formal review record. A retrospective note cannot add an approval to an already-merged PR. |
| Sprint 1 demo | **Done** | `Demo 1.mov` is 60.91 seconds. |
| Sprint 2 implementation freeze and deviations | **Done** | `PROJECT_CLOSEOUT.md` and `IMPLEMENTATION_DEVIATIONS.md`. |
| Sprint 2 demo | **Needs a compliant replacement** | `Demo 2.mov` is 157.03 seconds (2:37), exceeding the checklist's 2-minute requirement. |

## Part 3 — Testing and quality assurance

| Item | Status | Evidence |
|---|---|---|
| Backend automated tests | **Pass on PostgreSQL and SQLite** | On 11 November: SQLite ran 90 tests (89 passed, 1 PostgreSQL-only skip). On 10 November: PostgreSQL 18 ran all 90 tests successfully, including the concurrency test. |
| Test plan cases TC-001–TC-011 | **Pass** | Automated API coverage; see `TEST_PLAN_EXECUTION_ADDENDUM.md`. |
| TC-012 response time | **Pass for recorded local profile** | p95 47 ms; local SQLite/development server. |
| TC-013 500 concurrent students | **Pass for the recorded local profile** | 500/500 accounts authenticated; 12,788 requests; zero failures. Raw CSV and summary JSON are present in the local working tree under `../load_tests/evidence/2026-11-10/`; see `../load_tests/README.md`. |
| TC-014 99% availability | **Pass; complete by sample-count criterion** | All 360 recorded checks succeeded (100%), above the 99% target. Timestamp gaps are disclosed as context; see `SPRINT_2_AVAILABILITY_REPORT.md`. |
| TC-015 staff usability | **Workable; ready for participant testing, results pending** | A source walkthrough confirms the eight UI actions exist. Independent staff sessions are needed to measure the 90% target. |
| Unit/API, system validation, code coverage, branch coverage reports | **Done** | `UNIT_TEST_REPORT.md`, `SYSTEM_VALIDATION_REPORT.md`, `CODE_COVERAGE_REPORT.md`, and `BRANCH_COVERAGE_REPORT.md`. Application statement coverage is 93.1%; branch coverage is 67.7%. |

## Part 4 — Final evaluation and viva

| Item | Status | Evidence |
|---|---|---|
| Core implementation and readable/versioned codebase | **Done for repository evidence** | Backend API suite, frontend production build, Git history, and implementation documentation. |
| Explain implementation deviations | **Documented; team explanation remains a viva task** | `IMPLEMENTATION_DEVIATIONS.md` and the design addendum. |
| Team members explain individual code contributions, PRs, Agile process, and architecture | **Cannot be verified from files** | Requires the team viva. |

## Completion summary

The repository work is substantially complete: the missing design details and four requested testing report categories are documented, and targeted API tests cover profile, notice, allocation, and visitor paths. The full backend suite passes on PostgreSQL 18 and SQLite (with the expected SQLite-only concurrency skip), and the frontend production build passes.

Remaining validation work includes independent staff usability sessions, a 2-minute Sprint 2 demo, and the live board/review and oral viva checks. The repository history documents retrospective review records for some already-merged Sprint 1 PRs rather than formal reviews attached to those PRs. The connected GitHub capability cannot inspect the project board; the latest HEAD has no reported commit statuses, so hosted workflow success also remains unverified. TC-014 passed by the 360-check sampled success-rate criterion; the raw data's timestamp gaps are disclosed as context. The 500-user run has reproducible local raw evidence.
