from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from decimal import Decimal
from rest_framework import serializers
from .models import FeeRecord, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "amount", "payment_mode", "created_at")
        read_only_fields = ("id", "created_at")


class FeeRecordSerializer(serializers.ModelSerializer):
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    fee_status = serializers.CharField(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = FeeRecord
        fields = ("id", "total_amount", "amount_paid", "balance_due", "fee_status", "payments")
        read_only_fields = ("id", "total_amount", "amount_paid", "balance_due", "fee_status", "payments")


class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01"))
    payment_mode = serializers.ChoiceField(choices=Payment.PAYMENT_MODE_CHOICES, default="ONLINE_BANKING")

class StaffFeeRecordSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(role="STUDENT"),
        validators=[UniqueValidator(
            queryset=FeeRecord.objects.all(),
            message="This student already has a fee record.",
        )],
    )
    student_username = serializers.CharField(source="student.username", read_only=True)
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    fee_status = serializers.CharField(read_only=True)

    class Meta:
        model = FeeRecord
        fields = ("id", "student", "student_username", "total_amount",
                  "amount_paid", "balance_due", "fee_status")
        read_only_fields = ("id", "amount_paid", "balance_due", "fee_status")

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero.")
        if self.instance is not None and value < self.instance.amount_paid:
            raise serializers.ValidationError("Total amount cannot be less than the amount already paid.")
        return value

    def validate_student(self, value):
        if self.instance is not None and value != self.instance.student:
            raise serializers.ValidationError("The student on a fee record cannot be changed.")
        return value
