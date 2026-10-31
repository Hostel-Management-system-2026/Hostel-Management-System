from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import FeeRecord

User = get_user_model()


class FeeManagerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            username="student1", password="password123", role="STUDENT"
        )
        self.other_student = User.objects.create_user(
            username="student2", password="password123", role="STUDENT"
        )
        self.fee_record = FeeRecord.objects.create(
            student=self.student,
            total_amount=Decimal("10000.00")
        )

    def test_view_my_fee_statement_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/v1/fees/my")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["total_amount"]), Decimal("10000.00"))
        self.assertEqual(response.data["fee_status"], "UNPAID")

    def test_partial_payment_updates_balance_and_status(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post("/api/v1/fees/pay", {"amount": "4000.00", "payment_mode": "ONLINE_BANKING"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["balance_due"]), Decimal("6000.00"))
        self.assertEqual(response.data["fee_status"], "PARTIAL")

    def test_full_payment_marks_fee_paid(self):
        self.client.force_authenticate(user=self.student)
        self.client.post("/api/v1/fees/pay", {"amount": "6000.00", "payment_mode": "ONLINE_BANKING"})
        response = self.client.post("/api/v1/fees/pay", {"amount": "4000.00", "payment_mode": "ONLINE_BANKING"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["balance_due"]), Decimal("0.00"))
        self.assertEqual(response.data["fee_status"], "PAID")

    def test_payment_exceeding_balance_fails(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post("/api/v1/fees/pay", {"amount": "15000.00", "payment_mode": "ONLINE_BANKING"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_cannot_access_or_pay_other_student_fees(self):
        self.client.force_authenticate(user=self.other_student)
        response = self.client.get("/api/v1/fees/my")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class StaffFeeRecordTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user("admin1", password="password123", role="ADMIN")
        self.warden = User.objects.create_user("warden1", password="password123", role="WARDEN")
        self.student = User.objects.create_user("student9", password="password123", role="STUDENT")

    def create_record(self, total="12000.00"):
        self.client.force_authenticate(user=self.admin)
        return self.client.post(
            "/api/v1/fees/records",
            {"student": self.student.pk, "total_amount": total},
            format="json",
        )

    def test_admin_creates_record_and_student_can_then_view_it(self):
        self.client.force_authenticate(user=self.student)
        self.assertEqual(self.client.get("/api/v1/fees/my").status_code, 404)

        response = self.create_record()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["fee_status"], "UNPAID")

        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/v1/fees/my")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.data["balance_due"]), Decimal("12000.00"))

    def test_second_record_for_same_student_is_rejected(self):
        self.create_record()
        self.assertEqual(self.create_record().status_code, 400)

    def test_record_cannot_be_created_for_a_non_student(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/fees/records",
            {"student": self.warden.pk, "total_amount": "5000.00"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_student_and_warden_cannot_use_staff_endpoints(self):
        for user in (self.student, self.warden):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.get("/api/v1/fees/records").status_code, 403)
            response = self.client.post(
                "/api/v1/fees/records",
                {"student": self.student.pk, "total_amount": "1000.00"},
                format="json",
            )
            self.assertEqual(response.status_code, 403)

    def test_admin_can_list_and_update_total(self):
        record_id = self.create_record().data["id"]
        response = self.client.get("/api/v1/fees/records")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.patch(
            f"/api/v1/fees/records/{record_id}", {"total_amount": "15000.00"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.data["total_amount"]), Decimal("15000.00"))

    def test_total_cannot_drop_below_amount_already_paid(self):
        record_id = self.create_record().data["id"]
        FeeRecord.objects.filter(pk=record_id).update(amount_paid=Decimal("5000.00"))
        response = self.client.patch(
            f"/api/v1/fees/records/{record_id}", {"total_amount": "4000.00"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
