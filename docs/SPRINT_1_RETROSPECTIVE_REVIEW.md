# Sprint 1 retrospective review record

This is a retrospective record for the Sprint 1 pull requests. GitHub does not permit submitting a new formal review on a merged PR, so this document does not represent an approval attached to those PRs.

| PR | Feature | Retrospective status |
| --- | --- | --- |
| #23 | Visitor logging | Reviewed; Warden-only writes, required entry time, single exit update, and timestamp validation are covered by tests. |
| #24 | Weekly mess menu | Reviewed; role checks, menu validation, replacement by week, and latest-publication selection are covered by tests. |
| #25 | Leave requests | Reviewed; request ownership comes from the authenticated user, students see their own requests, and only wardens can decide a pending request. |
| #26 | Database role enforcement and menu validation | Reviewed; feature permissions use the authenticated database user's role. |
| #27 | Student profiles | Reviewed; students can read their own profile and admin operations are role-restricted. |
| #28 | Complaints | Reviewed; students create and track their own complaints, wardens make sequential transitions, and invalid transitions are rejected. |
| #29 | Student notices | Reviewed; admin mutations and published student visibility are role-restricted. |
| #30 | Authentication | Reviewed; password hashing, JWT login, and role enforcement have coverage. |
| #31 | Room allocation | Formal review recorded and approved. The follow-up now also serializes capacity checks under a database row lock. |

The repository had no CI workflows when these PRs were merged. The new workflow runs Django checks and the backend suite on PostgreSQL for pull requests and pushes to `main`. Future PRs should wait for CI and an owner approval before merge.
