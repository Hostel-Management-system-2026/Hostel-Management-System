# HMS backend

This backend follows the project Test Plan's proposed Django REST Framework and PostgreSQL stack. For local work, set up a virtual environment, install `requirements.txt`, copy `.env.example` into your environment, and run `python manage.py migrate` followed by `python manage.py runserver`.

The feature APIs use the shared authentication layer's role with canonical values `STUDENT`, `WARDEN`, or `ADMIN`. The permission helpers accept a `request.user.role` value, a verified JWT `role` claim, or Django groups with those names (an optional `ROLE_` prefix is accepted). The authentication issue must provide one of these trusted role sources and configure JWT authentication in Django REST Framework settings; clients must never choose their own role in a request body.

## Visitor logging API (issue #14)

- `POST /api/v1/visitors` (Warden): `visitor_name`, `student_id`, `room_number`, `entry_at` are required; `purpose` and `exit_at` are optional.
- `PATCH /api/v1/visitors/{id}/exit` (Warden): records the supplied `exit_at`, or the current UTC time when omitted. A second exit update returns a conflict.

The entry time is required and an active visit is represented by `exit_at: null`.

## Weekly mess menu API (issue #15)

- `POST /api/v1/mess/menu` (Admin): publish or replace the menu for a `week_start` date. `menu` must contain all seven days, each with non-empty `breakfast`, `lunch`, and `dinner` lists of item names.
- `GET /api/v1/mess/menu` (Student, Warden, or Admin): return the most recently published weekly menu.

Example `menu`: `{"days":{"Monday":{"breakfast":["Idli"],"lunch":["Rice"],"dinner":["Roti"]},"Tuesday":{"breakfast":["Poha"],"lunch":["Dal"],"dinner":["Rice"]},"Wednesday":{"breakfast":["Upma"],"lunch":["Rice"],"dinner":["Roti"]},"Thursday":{"breakfast":["Idli"],"lunch":["Dal"],"dinner":["Rice"]},"Friday":{"breakfast":["Poha"],"lunch":["Rice"],"dinner":["Roti"]},"Saturday":{"breakfast":["Upma"],"lunch":["Rice"],"dinner":["Roti"]},"Sunday":{"breakfast":["Dosa"],"lunch":["Rice"],"dinner":["Paneer"]}}}`. The API keeps one published menu per week start date.

## Leave and outpass API (issue #16)

- `POST /api/v1/leave` (Student): submit `start_date`, `end_date`, and `reason`. The request stores a foreign key to the authenticated account and starts as `PENDING`; the client cannot choose the owner.
- `GET /api/v1/leave` (Student or Warden): students see their own requests; wardens see requests awaiting their decision and completed requests.
- `PATCH /api/v1/leave/{id}/decision` (Warden): send `{"decision":"approve"}` or `{"decision":"reject"}`. A request cannot be decided twice.

Only Warden decisions can move a request from `PENDING` to `APPROVED` or `REJECTED`.
