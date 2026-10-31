
import csv
import itertools
import os
from pathlib import Path

from locust import HttpUser, between, task

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = Path(
    os.getenv(
        "STUDENT_CREDENTIALS_FILE",
        str(BASE_DIR / "data" / "students.csv"),
    )
)

LOGIN_URL = "/api/v1/auth/login/"

_credentials = []
_user_counter = itertools.count()


def load_students():
    if not CREDENTIALS_FILE.exists():
        raise RuntimeError(
            f"Credentials file not found: {CREDENTIALS_FILE}"
        )

    with CREDENTIALS_FILE.open(
        newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        if not {"username", "password"}.issubset(
            reader.fieldnames or []
        ):
            raise RuntimeError(
                "CSV must contain username,password columns."
            )

        students = [
            {
                "username": row["username"].strip(),
                "password": row["password"].strip(),
            }
            for row in reader
            if row.get("username", "").strip()
            and row.get("password", "").strip()
        ]

    if not students:
        raise RuntimeError("No student accounts found.")

    return students


_credentials = load_students()


class HostelStudentUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        index = next(_user_counter)

        if index >= len(_credentials):
            raise RuntimeError(
                "Insufficient student accounts for load test."
            )

        student = _credentials[index]

        response = self.client.post(
            LOGIN_URL,
            json={
                "username": student["username"],
                "password": student["password"],
            },
            name="Authentication / Login",
        )

        if response.status_code != 200:
            response.failure("Student authentication failed.")
            raise RuntimeError("Login failed.")

        try:
            token = response.json()["access"]
        except (ValueError, KeyError):
            response.failure("Access token missing.")
            raise RuntimeError("Invalid login response.")

        self.client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

    @task(4)
    def view_profile(self):
        self.client.get(
            "/api/v1/profiles/me",
            name="Student / Profile",
        )

    @task(4)
    def view_notices(self):
        self.client.get(
            "/api/v1/notices",
            name="Student / Notices",
        )

    @task(4)
    def view_mess_menu(self):
        self.client.get(
            "/api/v1/mess/menu",
            name="Student / Mess Menu",
        )

    @task(3)
    def view_facilities(self):
        self.client.get(
            "/api/v1/facilities/",
            name="Student / Facilities",
        )

    @task(3)
    def view_leave_requests(self):
        self.client.get(
            "/api/v1/leave",
            name="Student / Leave Requests",
        )

    @task(3)
    def view_complaints(self):
        self.client.get(
            "/api/v1/complaints",
            name="Student / Complaints",
        )
