from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from common.permissions import IsAdmin

from .models import User


class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"ok": True})


class AuthAndRoleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.users = {
            "ADMIN": User.objects.create_user("admin1", password="Admin@12345", role="ADMIN"),
            "WARDEN": User.objects.create_user("warden1", password="Warden@12345", role="WARDEN"),
            "STUDENT": User.objects.create_user("student1", password="Student@12345", role="STUDENT"),
        }
        self.passwords = {"admin1": "Admin@12345", "warden1": "Warden@12345", "student1": "Student@12345"}

    def login(self, username, password):
        return self.client.post(
            "/api/v1/auth/login/",
            {"username": username, "password": password},
            format="json",
        )

    def call_admin_view(self, token=None):
        request = self.factory.get("/admin-only/")
        if token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        return AdminOnlyView.as_view()(request)

    def test_all_three_roles_can_log_in_and_token_carries_role(self):
        for role, user in self.users.items():
            resp = self.login(user.username, self.passwords[user.username])
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(AccessToken(resp.data["access"])["role"], role)

    def test_wrong_password_rejected(self):
        resp = self.login("admin1", "wrong-password")
        self.assertEqual(resp.status_code, 401)

    def test_passwords_are_hashed_not_plaintext(self):
        for user in self.users.values():
            self.assertNotEqual(user.password, self.passwords[user.username])
            self.assertTrue(user.password.startswith("pbkdf2_"))
            self.assertTrue(user.check_password(self.passwords[user.username]))

    def test_no_token_is_rejected_with_401(self):
        self.assertEqual(self.call_admin_view().status_code, 401)

    def test_student_is_forbidden_from_admin_action(self):
        token = self.login("student1", "Student@12345").data["access"]
        self.assertEqual(self.call_admin_view(token).status_code, 403)

    def test_warden_is_forbidden_from_admin_action(self):
        token = self.login("warden1", "Warden@12345").data["access"]
        self.assertEqual(self.call_admin_view(token).status_code, 403)

    def test_admin_is_allowed_on_admin_action(self):
        token = self.login("admin1", "Admin@12345").data["access"]
        self.assertEqual(self.call_admin_view(token).status_code, 200)
