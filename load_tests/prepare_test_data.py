"""Prepare the one read-only menu fixture required by the student load profile."""

import os
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if os.environ.get("HMS_DB_ENGINE", "sqlite").lower() == "postgresql":
    raise SystemExit("Refusing to seed the PostgreSQL database; use local SQLite.")
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from mess.models import WeeklyMenu  # noqa: E402


days = (
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
)
menu_payload = {
    "days": {
        day: {
            "breakfast": ["Test breakfast"],
            "lunch": ["Test lunch"],
            "dinner": ["Test dinner"],
        }
        for day in days
    }
}
menu, created = WeeklyMenu.objects.get_or_create(
    week_start=date(2026, 11, 9), defaults={"menu": menu_payload}
)
print(f"{'Created' if created else 'Using existing'} synthetic weekly menu id={menu.pk}")
