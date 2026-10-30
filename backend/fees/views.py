from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsStudent
from .models import FeeRecord, Payment
from .serializers import FeeRecordSerializer, PaymentCreateSerializer


class StudentFeeView(APIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request):
        try:
            fee_record = request.user.fee_record
        except FeeRecord.DoesNotExist:
            return Response({"detail": "Fee record not found for student."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeeRecordSerializer(fee_record)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecordPaymentView(APIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request):
        try:
            fee_record = request.user.fee_record
        except FeeRecord.DoesNotExist:
            return Response({"detail": "Fee record not found for student."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        payment_mode = serializer.validated_data["payment_mode"]

        with transaction.atomic():
            fee_record = FeeRecord.objects.select_for_update().get(pk=fee_record.pk)

            if amount > fee_record.balance_due:
                raise ValidationError({"amount": "Payment amount cannot exceed the remaining balance."})

            payment = Payment.objects.create(
                fee_record=fee_record,
                amount=amount,
                payment_mode=payment_mode
            )

            fee_record.amount_paid += amount
            fee_record.save()

        return Response(FeeRecordSerializer(fee_record).data, status=status.HTTP_201_CREATED)