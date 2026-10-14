from types import SimpleNamespace

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Notice

class NoticeApiTests(TestCase):
def setUp(self):
self.client = APIClient()
self.admin = SimpleNamespace(
pk="admin-1", role="ADMIN", is_authenticated=True
)
self.student = SimpleNamespace(
pk="student-1", role="STUDENT", is_authenticated=True
)
self.notice = Notice.objects.create(
title="Hostel meeting",
body="Meeting at 5 PM.",
audience="ALL_STUDENTS",
is_published=True,
published_by="admin-1",
)

```
def test_admin_can_publish_notice(self):
    self.client.force_authenticate(self.admin)
    response = self.client.post(
        "/api/v1/notices",
        {
            "title": "Holiday notice",
            "body": "The hostel office will be closed.",
            "audience": "ALL_STUDENTS",
            "is_published": True,
        },
        format="json",
    )
    self.assertEqual(response.status_code, 201)

def test_student_cannot_publish_notice(self):
    self.client.force_authenticate(self.student)
    response = self.client.post(
        "/api/v1/notices",
        {"title": "Unauthorized", "body": "Test"},
        format="json",
    )
    self.assertEqual(response.status_code, 403)

def test_student_can_view_published_notice(self):
    self.client.force_authenticate(self.student)
    response = self.client.get("/api/v1/notices")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)

def test_student_cannot_view_unpublished_notice(self):
    Notice.objects.create(
        title="Draft",
        body="Not published",
        audience="ALL_STUDENTS",
        is_published=False,
        published_by="admin-1",
    )
    self.client.force_authenticate(self.student)
    response = self.client.get("/api/v1/notices")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)

def test_jwt_role_cannot_replace_missing_user_role(self):
    user_without_role = SimpleNamespace(
        pk="unknown-1", is_authenticated=True
    )
    self.client.force_authenticate(
        user=user_without_role,
        token={"role": "ADMIN"},
    )
    response = self.client.get("/api/v1/notices")
    self.assertEqual(response.status_code, 403)

def test_student_cannot_view_notice_for_other_audience(self):
    private_notice = Notice.objects.create(
        title="Warden notice",
        body="For wardens only.",
        audience="WARDENS",
        is_published=True,
        published_by="admin-1",
    )
    self.client.force_authenticate(self.student)
    response = self.client.get(
        f"/api/v1/notices/{private_notice.pk}"
    )
    self.assertEqual(response.status_code, 403)

def test_unauthenticated_user_cannot_view_notices(self):
    response = self.client.get("/api/v1/notices")
    self.assertIn(response.status_code, (401, 403))
```
