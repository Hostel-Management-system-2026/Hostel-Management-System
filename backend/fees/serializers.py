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