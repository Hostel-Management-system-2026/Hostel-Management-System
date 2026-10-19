# Implementation deviations

This record tracks differences between the submitted Software Design Specification (SDS) and the Sprint 1 implementation. The changes below must be explained in the Sprint 1 demonstration. Team members should confirm the rationale before the final submission.

## Student profile API routes

The SDS endpoint matrix described profile access as `GET /api/v1/profiles/{student_id}` and profile maintenance as `PUT /api/v1/profiles/{student_id}`. The implementation instead uses:

- `GET /api/v1/profiles/me` for a student's own read-only profile.
- `GET` and `POST /api/v1/profiles` for admin listing and creation.
- `GET`, `PUT`, `PATCH`, and `DELETE /api/v1/profiles/{profile_id}` for admin maintenance.

The route split makes the student's self-service operation explicit and reserves collection and record-management operations for admins. Confirm this rationale and the accepted endpoint contract with the team before the final demo.

## Room capacity concurrency

The room allocation serializer originally checked room occupancy before creating an allocation, which could allow simultaneous requests to exceed capacity. The remediation adds a transactional row lock and repeats the capacity check while holding that lock. A PostgreSQL concurrency regression test is included with the CI remediation.
