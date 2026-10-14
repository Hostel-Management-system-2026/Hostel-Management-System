from types import SimpleNamespace

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Complaint

class ComplaintApiTests(TestCase):
def setUp(self):
self.client = APIClient()
self.student = SimpleNamespace(
pk="student-1", role="STUDENT", is_authenticated=True
)
self.warden = SimpleNamespace(
pk="warden-1", role="WARDEN", is_authenticated=True
)
self.payload = {
"title": "Broken light",
"description": "The light in my room is not working.",
}

```
def test_student_can_register_complaint_as_open(self):
    self.client.force_authenticate(self.student)

    response = self.client.post(
        "/api/v1/complaints", self.payload, format="json"
    )

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data["status"], Complaint.Status.OPEN)
    self.assertEqual(response.data["student_id"], "student-1")

def test_student_cannot_choose_status_or_owner(self):
    self.client.force_authenticate(self.student)

    response = self.client.post(
        "/api/v1/complaints",
        {
            **self.payload,
            "student_id": "someone-else",
            "status": "RESOLVED",
        },
        format="json",
    )

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data["student_id"], "student-1")
    self.assertEqual(response.data["status"], Complaint.Status.OPEN)

def test_student_cannot_update_complaint_status(self):
    complaint = Complaint.objects.create(
        student_id="student-1",
        title="Broken light",
        description="The light is broken.",
    )
    self.client.force_authenticate(self.student)

    response = self.client.patch(
        f"/api/v1/complaints/{complaint.pk}",
        {"status": "IN_PROGRESS"},
        format="json",
    )

    self.assertEqual(response.status_code, 403)

def test_warden_can_move_open_complaint_to_in_progress(self):
    complaint = Complaint.objects.create(
        student_id="student-1",
        title="Broken light",
        description="The light is broken.",
    )
    self.client.force_authenticate(self.warden)

    response = self.client.patch(
        f"/api/v1/complaints/{complaint.pk}",
        {"status": "IN_PROGRESS"},
        format="json",
    )

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["status"], Complaint.Status.IN_PROGRESS)

def test_warden_cannot_skip_required_status(self):
    complaint = Complaint.objects.create(
        student_id="student-1",
        title="Broken light",
        description="The light is broken.",
    )
    self.client.force_authenticate(self.warden)

    response = self.client.patch(
        f"/api/v1/complaints/{complaint.pk}",
        {"status": "RESOLVED"},
        format="json",
    )

    self.assertEqual(response.status_code, 409)
    complaint.refresh_from_db()
    self.assertEqual(complaint.status, Complaint.Status.OPEN)

def test_unauthenticated_user_cannot_register_complaint(self):
    response = self.client.post(
        "/api/v1/complaints", self.payload, format="json"
    )

    self.assertIn(response.status_code, (401, 403))
```
