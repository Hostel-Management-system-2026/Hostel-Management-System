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