from datetime import date, timedelta
from types import SimpleNamespace

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import WeeklyMenu


def weekly_menu():
    return {
        "days": {
            day: {
                "breakfast": ["Idli"],
                "lunch": ["Rice"],
                "dinner": ["Roti"],
            }
            for day in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        }
    }


class WeeklyMenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = SimpleNamespace(pk="admin-1", role="ADMIN", is_authenticated=True)
        self.student = SimpleNamespace(pk="student-1", role="STUDENT", is_authenticated=True)
        self.warden = SimpleNamespace(pk="warden-1", role="WARDEN", is_authenticated=True)
        self.payload = {"week_start": "2026-10-19", "menu": weekly_menu()}

    def test_admin_can_publish_menu(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post("/api/v1/mess/menu", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(WeeklyMenu.objects.count(), 1)

    def test_non_admin_cannot_publish_menu(self):
        for user in (self.student, self.warden):
            self.client.force_authenticate(user)
            response = self.client.post("/api/v1/mess/menu", self.payload, format="json")
            self.assertEqual(response.status_code, 403)
        self.assertEqual(WeeklyMenu.objects.count(), 0)

    def test_student_warden_and_admin_can_view_menu(self):
        menu = WeeklyMenu.objects.create(week_start=date(2026, 10, 19), menu=weekly_menu())

        for user in (self.student, self.warden, self.admin):
            self.client.force_authenticate(user)
            response = self.client.get("/api/v1/mess/menu")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["id"], menu.pk)

    def test_latest_published_menu_is_returned_not_latest_week_date(self):
        published_now = timezone.now()
        newer_week = WeeklyMenu.objects.create(week_start=date(2026, 10, 26), menu=weekly_menu())
        older_week = WeeklyMenu.objects.create(week_start=date(2026, 10, 19), menu=weekly_menu())
        WeeklyMenu.objects.filter(pk=newer_week.pk).update(published_at=published_now - timedelta(days=1))
        WeeklyMenu.objects.filter(pk=older_week.pk).update(published_at=published_now)
        self.client.force_authenticate(self.student)

        response = self.client.get("/api/v1/mess/menu")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], older_week.pk)

    def test_publishing_existing_week_replaces_its_menu(self):
        self.client.force_authenticate(self.admin)
        first = self.client.post("/api/v1/mess/menu", self.payload, format="json")
        replacement = weekly_menu()
        replacement["days"]["Monday"]["breakfast"] = ["Upma"]

        response = self.client.post(
            "/api/v1/mess/menu",
            {**self.payload, "menu": replacement},
            format="json",
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], first.data["id"])
        self.assertEqual(WeeklyMenu.objects.count(), 1)
        self.assertEqual(response.data["menu"], replacement)

    def test_invalid_weekly_menu_structure_is_rejected(self):
        self.client.force_authenticate(self.admin)
        invalid_menu = {"days": {"Monday": {"breakfast": "Idli"}}}

        response = self.client.post(
            "/api/v1/mess/menu",
            {**self.payload, "menu": invalid_menu},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(WeeklyMenu.objects.count(), 0)
