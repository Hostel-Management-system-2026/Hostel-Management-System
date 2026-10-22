# HMS frontend

The React + TypeScript web client lives here. It is based on the API routes available on `main`.

## Start locally

1. Start Django from `backend/` with `python manage.py runserver`.
2. In this directory, run `npm install`, then `npm run dev`.
3. Open the Vite URL shown in the terminal. The development server proxies `/api` to `http://127.0.0.1:8000`; override that target with `VITE_BACKEND_ORIGIN` in `.env.local` if needed.

Copy `.env.example` to `.env.local` only when the defaults need changing. `VITE_API_BASE_URL` is the API prefix used by the shared client.

## Shared contracts

- `src/api/client.ts` exports `api.get`, `api.post`, `api.patch`, `api.put`, and `api.delete`. It adds the bearer access token, converts server errors to `ApiError`, refreshes once after a 401, and clears the stored session if refresh fails.
- `src/auth/AuthContext.tsx` exports `useAuth()` with `role`, `signIn`, and `signOut`.
- The backend login is `POST /api/v1/auth/login/` with `{ "username": "...", "password": "..." }`. It returns SimpleJWT `access` and `refresh` tokens. The access token's role is used only to choose client navigation. The API remains authoritative and enforces permissions.
- `RequireRole` protects routes. Add feature routes in `src/App.tsx` and role-filtered links in `navItems`.
- Put feature components in `src/features/<feature>/`; keep module-specific calls in the module's `api.ts` and share only generic HTTP/auth code.

## API areas available on this base

| Area | Available backend contract |
| --- | --- |
| Profiles | `GET /profiles/me`, collection `GET/POST /profiles`, detail `GET/PUT/PATCH/DELETE /profiles/{id}` |
| Complaints | `GET/POST /complaints`, detail status transition `PATCH /complaints/{id}` |
| Notices | `GET/POST /notices`, detail `GET/PATCH/DELETE /notices/{id}` |
| Room allocations | inventory `GET /rooms/`, allocations `GET/POST /allocations/`, release `PATCH /allocations/{id}/release` |
| Visitors | `GET/POST /visitors`, exit `PATCH /visitors/{id}/exit` |
| Mess menu | `GET/POST /mess/menu` |
| Leave requests | `GET/POST /leave`, decision `PATCH /leave/{id}/decision` |

There is no password recovery endpoint on this base. Don't present that unavailable flow as working.

## Frontend implementation status

The current client includes role-specific workflows for profiles, complaints, notices, room allocations, visitor check-in/check-out and history, weekly menus, and leave requests. The allocation screen uses live room capacity and occupancy data; the visitor screen can filter current and completed visits.

Allocation creation still uses the numeric student account ID accepted by the API. Password recovery is unavailable because there is no backend route for it.
