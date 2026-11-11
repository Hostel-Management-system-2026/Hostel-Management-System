"""Remove only synthetic fixtures created for the local load-test run."""

import csv
import os
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if os.environ.get("HMS_DB_ENGINE", "sqlite").lower() == "postgresql":
    raise SystemExit("Refusing to clean the PostgreSQL database; use local SQLite.")
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from accounts.models import User  # noqa: E402
from mess.models import WeeklyMenu  # noqa: E402


days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
synthetic_menu = {
    "days": {
        day: {
            "breakfast": ["Test breakfast"],
            "lunch": ["Test lunch"],
            "dinner": ["Test dinner"],
        }
        for day in days
    }
}
reserved_names = [f"loadtest_{number:04d}" for number in range(1, 501)]
test_users = User.objects.filter(username__in=reserved_names)
user_count = test_users.count()
test_users.delete()
menu_count, _ = WeeklyMenu.objects.filter(
    week_start=date(2026, 11, 9), menu=synthetic_menu
).delete()

credentials = ROOT / "load_tests" / "data" / "students.csv"
if credentials.exists():
    credentials.unlink()

print(f"Removed {user_count} synthetic load-test users and {menu_count} matching menu rows.")
print(f"Removed credentials file: {credentials.exists() is False}")
