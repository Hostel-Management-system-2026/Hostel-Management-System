# HMS backend

This backend follows the project Test Plan's proposed Django REST Framework and PostgreSQL stack. For local work, set up a virtual environment, install `requirements.txt`, copy `.env.example` into your environment, and run `python manage.py migrate` followed by `python manage.py runserver`.

The feature APIs use the shared authentication layer's `request.user.role` value (or its JWT `role` claim) with `STUDENT`, `WARDEN`, or `ADMIN`. The authentication issue should expose one of these role values and configure JWT authentication in Django REST Framework settings.

## Visitor logging API (issue #14)

- `POST /api/v1/visitors` (Warden): `visitor_name`, `student_id`, `room_number`, `entry_at` are required; `purpose` and `exit_at` are optional.
- `PATCH /api/v1/visitors/{id}/exit` (Warden): records the supplied `exit_at`, or the current UTC time when omitted. A second exit update returns a conflict.

The entry time is required and an active visit is represented by `exit_at: null`.
