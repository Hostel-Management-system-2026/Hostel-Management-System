from django.urls import path
from .views import StudentFeeView, RecordPaymentView

urlpatterns = [
    path("fees/my", StudentFeeView.as_view(), name="student-fee-detail"),
    path("fees/pay", RecordPaymentView.as_view(), name="record-payment"),
]