"""Seed an isolated local fixture and print a benchmark-only JWT."""

import os
import secrets
import sys
from datetime import timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if os.environ.get("HMS_DB_ENGINE", "sqlite").lower() == "postgresql":
    raise SystemExit("Refusing to seed the PostgreSQL database; use a local SQLite development database.")

sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from accounts.models import User  # noqa: E402
from complaints.models import Complaint  # noqa: E402
from rest_framework_simplejwt.tokens import AccessToken  # noqa: E402


username = f"sprint2_perf_student_{secrets.token_hex(8)}"
user = User.objects.create_user(
    username=username,
    password=secrets.token_urlsafe(24),
    role=User.Role.STUDENT,
)

Complaint.objects.filter(student_id=str(user.pk), title__startswith="Perf fixture").delete()
Complaint.objects.bulk_create(
    [
        Complaint(
            student_id=str(user.pk),
            title=f"Perf fixture {index}",
            description="Representative response-time benchmark record " * 5,
            status=Complaint.Status.OPEN,
        )
        for index in range(100)
    ]
)

token = AccessToken.for_user(user)
token.set_exp(lifetime=timedelta(minutes=20))
print(f"Benchmark account: {username}", file=sys.stderr)
print(token)
