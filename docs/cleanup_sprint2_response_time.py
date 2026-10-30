"""Remove one benchmark fixture account and its generated complaints."""

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if os.environ.get("HMS_DB_ENGINE", "sqlite").lower() == "postgresql":
    raise SystemExit("Refusing to modify the PostgreSQL database; use the local SQLite database.")

parser = argparse.ArgumentParser()
parser.add_argument("username", help="exact account name printed by the fixture preparation script")
args = parser.parse_args()
if not args.username.startswith("sprint2_perf_student_"):
    parser.error("username must be a Sprint 2 benchmark fixture account")

sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from accounts.models import User  # noqa: E402
from complaints.models import Complaint  # noqa: E402


user = User.objects.filter(username=args.username, role=User.Role.STUDENT).first()
if user is None:
    print("No matching benchmark student found; nothing removed.")
    raise SystemExit(0)

deleted_complaints, _ = Complaint.objects.filter(
    student_id=str(user.pk),
    title__startswith="Perf fixture",
).delete()
user.delete()
print(f"Removed benchmark student {args.username} and {deleted_complaints} fixture complaints.")
