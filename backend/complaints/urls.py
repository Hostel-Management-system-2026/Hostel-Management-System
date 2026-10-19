from django.urls import path

from .views import ComplaintCollectionView, ComplaintDetailView

urlpatterns = [
    path("complaints", ComplaintCollectionView.as_view(), name="complaint-list-create"),
    path("complaints/<int:complaint_id>", ComplaintDetailView.as_view(), name="complaint-detail"),
]
