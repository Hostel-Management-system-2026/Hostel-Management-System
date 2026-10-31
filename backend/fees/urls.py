from django.urls import path

from .views import (
    RecordPaymentView,
    StaffFeeRecordDetailView,
    StaffFeeRecordListCreateView,
    StudentFeeView,
)

urlpatterns = [
    path("fees/my", StudentFeeView.as_view(), name="student-fee-detail"),
    path("fees/pay", RecordPaymentView.as_view(), name="record-payment"),
    path("fees/records", StaffFeeRecordListCreateView.as_view(), name="staff-fee-records"),
    path("fees/records/<int:pk>", StaffFeeRecordDetailView.as_view(), name="staff-fee-record-detail"),
]
