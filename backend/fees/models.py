from django.db import models

# Create your models here.
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class FeeRecord(models.Model):
    STATUS_CHOICES = (
        ("UNPAID", "Unpaid"),
        ("PARTIAL", "Partial"),
        ("PAID", "Paid"),
    )

    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="fee_record"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance_due(self):
        return max(Decimal("0.00"), self.total_amount - self.amount_paid)

    @property
    def fee_status(self):
        if self.amount_paid == Decimal("0.00"):
            return "UNPAID"
        elif self.amount_paid < self.total_amount:
            return "PARTIAL"
        return "PAID"

    def __str__(self):
        return f"Fee Record for {self.student.username} - Status: {self.fee_status}"


class Payment(models.Model):
    PAYMENT_MODE_CHOICES = (
        ("ONLINE_BANKING", "Online Banking"),
        ("CARD", "Card"),
        ("UPI", "UPI"),
        ("CASH", "Cash"),
    )

    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=32, choices=PAYMENT_MODE_CHOICES, default="ONLINE_BANKING")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError({"amount": "Payment amount must be greater than zero."})
        if self.amount > self.fee_record.balance_due:
            raise ValidationError({"amount": "Payment amount cannot exceed the remaining balance."})

    def __str__(self):
        return f"Payment of {self.amount} for {self.fee_record.student.username}"