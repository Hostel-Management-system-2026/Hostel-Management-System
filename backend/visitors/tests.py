from datetime import timedelta
from types import SimpleNamespace

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import VisitorLog


class VisitorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.warden = SimpleNamespace(pk="warden-1", role="WARDEN", is_authenticated=True)
        self.student = SimpleNamespace(pk="student-1", role="STUDENT", is_authenticated=True)
        self.payload = {
            "visitor_name": "Morgan Lee",
            "student_id": "student-1",
            "room_number": "A-204",
            "entry_at": timezone.now().isoformat(),
        }

    def test_warden_can_create_visitor_log(self):
        self.client.force_authenticate(self.warden)

        response = self.client.post("/api/v1/visitors", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.data["exit_at"])
        self.assertEqual(VisitorLog.objects.count(), 1)

    def test_student_cannot_create_visitor_log(self):
        self.client.force_authenticate(self.student)

        response = self.client.post("/api/v1/visitors", self.payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(VisitorLog.objects.count(), 0)

    def test_missing_entry_timestamp_is_rejected(self):
        self.client.force_authenticate(self.warden)
        payload = {key: value for key, value in self.payload.items() if key != "entry_at"}

        response = self.client.post("/api/v1/visitors", payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_exit_before_entry_is_rejected(self):
        record = VisitorLog.objects.create(
            visitor_name="Morgan Lee",
            student_id="student-1",
            room_number="A-204",
            entry_at=timezone.now(),
        )
        self.client.force_authenticate(self.warden)

        response = self.client.patch(
            f"/api/v1/visitors/{record.pk}/exit",
            {"exit_at": (record.entry_at - timedelta(minutes=1)).isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        record.refresh_from_db()
        self.assertIsNone(record.exit_at)

    def test_malformed_exit_timestamp_is_rejected(self):
        record = VisitorLog.objects.create(
            visitor_name="Morgan Lee",
            student_id="student-1",
            room_number="A-204",
            entry_at=timezone.now() - timedelta(minutes=5),
        )
        self.client.force_authenticate(self.warden)

        response = self.client.patch(
            f"/api/v1/visitors/{record.pk}/exit",
            {"exit_at": "not-a-timestamp"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        record.refresh_from_db()
        self.assertIsNone(record.exit_at)

    def test_student_cannot_record_visitor_exit(self):
        record = VisitorLog.objects.create(
            visitor_name="Morgan Lee",
            student_id="student-1",
            room_number="A-204",
            entry_at=timezone.now() - timedelta(minutes=5),
        )
        self.client.force_authenticate(self.student)

        response = self.client.patch(f"/api/v1/visitors/{record.pk}/exit", {}, format="json")

        self.assertEqual(response.status_code, 403)
        record.refresh_from_db()
        self.assertIsNone(record.exit_at)

    def test_only_one_exit_update_succeeds(self):
        record = VisitorLog.objects.create(
            visitor_name="Morgan Lee",
            student_id="student-1",
            room_number="A-204",
            entry_at=timezone.now() - timedelta(minutes=5),
        )
        self.client.force_authenticate(self.warden)

        first = self.client.patch(f"/api/v1/visitors/{record.pk}/exit", {}, format="json")
        second = self.client.patch(f"/api/v1/visitors/{record.pk}/exit", {}, format="json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 409)

