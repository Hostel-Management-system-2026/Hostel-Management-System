from django.urls import path

from .views import LeaveDecisionView, LeaveRequestCollectionView


urlpatterns = [
    path("leave", LeaveRequestCollectionView.as_view(), name="leave-list-create"),
    path("leave/<int:leave_id>/decision", LeaveDecisionView.as_view(), name="leave-decision"),
]
