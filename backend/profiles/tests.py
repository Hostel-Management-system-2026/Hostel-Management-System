
from types import SimpleNamespace

from django.test import TestCase
from rest_framework.test import APIClient

from .models import StudentProfile


class StudentProfileApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = SimpleNamespace(
            pk="student-1",
            role="STUDENT",
            is_authenticated=True,
        )
        self.admin = SimpleNamespace(
            pk="admin-1",
            role="ADMIN",
            is_authenticated=True,
        )
        self.profile = StudentProfile.objects.create(
            user_id="student-1",
            student_number="S1001",
            full_name="Test Student",
            email="student@example.com",
        )

    def test_student_can_view_own_profile(self):
        self.client.force_authenticate(self.student)

        response = self.client.get("/api/v1/profiles/me")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["student_number"], "S1001")

    def test_student_without_profile_gets_404(self):
        self.client.force_authenticate(
            SimpleNamespace(
                pk="student-2",
                role="STUDENT",
                is_authenticated=True,
            )
        )

        response = self.client.get("/api/v1/profiles/me")

        self.assertEqual(response.status_code, 404)

    def test_student_cannot_list_all_profiles(self):
        self.client.force_authenticate(self.student)

        response = self.client.get("/api/v1/profiles")

        self.assertEqual(response.status_code, 403)

    def test_admin_can_list_profiles(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get("/api/v1/profiles")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_create_profile(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            "/api/v1/profiles",
            {
                "user_id": "student-2",
                "student_number": "S1002",
                "full_name": "Another Student",
                "email": "another@example.com",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            StudentProfile.objects.filter(student_number="S1002").exists()
        )

    def test_student_self_service_profile_is_read_only(self):
        self.client.force_authenticate(self.student)

        put_response = self.client.put(
            "/api/v1/profiles/me",
            {"full_name": "Changed Name"},
            format="json",
        )
        patch_response = self.client.patch(
            "/api/v1/profiles/me",
            {"full_name": "Changed Name"},
            format="json",
        )
        delete_response = self.client.delete("/api/v1/profiles/me")

        self.assertEqual(put_response.status_code, 403)
        self.assertEqual(patch_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, "Test Student")

    def test_admin_can_read_update_and_delete_profile(self):
        self.client.force_authenticate(self.admin)

        detail_url = f"/api/v1/profiles/{self.profile.pk}"
        read_response = self.client.get(detail_url)
        patch_response = self.client.patch(
            detail_url,
            {"full_name": "Updated Student"},
            format="json",
        )
        put_response = self.client.put(
            detail_url,
            {
                "user_id": "student-1",
                "student_number": "S1001",
                "full_name": "Replaced Student",
                "email": "replaced@example.com",
            },
            format="json",
        )
        delete_response = self.client.delete(detail_url)

        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(StudentProfile.objects.filter(pk=self.profile.pk).exists())

    def test_unauthenticated_user_cannot_view_profile(self):
        response = self.client.get("/api/v1/profiles/me")

        self.assertIn(response.status_code, (401, 403))
