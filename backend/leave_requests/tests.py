from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import LeaveRequest


class LeaveRequestApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()
        self.student = user_model.objects.create_user(username="student-1", password="secret")
        self.other_student = user_model.objects.create_user(username="student-2", password="secret")
        self.warden = user_model.objects.create_user(username="warden-1", password="secret")
        self.warden.role = "WARDEN"
        self.warden.save()
        self.payload = {
            "start_date": "2026-10-20",
            "end_date": "2026-10-22",
            "reason": "Family visit",
        }

    def test_student_submission_starts_pending_and_is_owned_by_auth_user(self):
        self.client.force_authenticate(self.student)

        response = self.client.post("/api/v1/leave", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], LeaveRequest.Status.PENDING)
        self.assertEqual(response.data["student_id"], self.student.pk)
        self.assertIsNone(response.data["decided_by"])

    def test_client_cannot_choose_another_student_as_owner(self):
        self.client.force_authenticate(self.student)

        response = self.client.post(
            "/api/v1/leave",
            {**self.payload, "student_id": self.other_student.pk},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["student_id"], self.student.pk)

    def test_student_only_sees_own_requests(self):
        own = LeaveRequest.objects.create(
            student=self.student,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 21),
            reason="Family visit",
        )
        LeaveRequest.objects.create(
            student=self.other_student,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 21),
            reason="Family visit",
        )
        self.client.force_authenticate(self.student)

        response = self.client.get("/api/v1/leave")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [own.pk])

    def test_warden_can_approve_and_is_recorded_as_decider(self):
        leave_request = LeaveRequest.objects.create(
            student=self.student,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 21),
            reason="Family visit",
        )
        self.client.force_authenticate(self.warden)

        response = self.client.patch(
            f"/api/v1/leave/{leave_request.pk}/decision",
            {"decision": "approve"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LeaveRequest.Status.APPROVED)
        self.assertEqual(response.data["decided_by"], self.warden.pk)

    def test_student_cannot_decide_leave_request(self):
        leave_request = LeaveRequest.objects.create(
            student=self.student,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 21),
            reason="Family visit",
        )
        self.client.force_authenticate(self.student)

        response = self.client.patch(
            f"/api/v1/leave/{leave_request.pk}/decision",
            {"decision": "approve"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_request_cannot_be_decided_twice(self):
        leave_request = LeaveRequest.objects.create(
            student=self.student,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 21),
            reason="Family visit",
            status=LeaveRequest.Status.APPROVED,
        )
        self.client.force_authenticate(self.warden)

        response = self.client.patch(
            f"/api/v1/leave/{leave_request.pk}/decision",
            {"decision": "reject"},
            format="json",
        )

        self.assertEqual(response.status_code, 409)

    def test_end_date_before_start_date_is_rejected(self):
        self.client.force_authenticate(self.student)

        response = self.client.post(
            "/api/v1/leave",
            {"start_date": "2026-10-22", "end_date": "2026-10-20", "reason": "Family visit"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(LeaveRequest.objects.count(), 0)
