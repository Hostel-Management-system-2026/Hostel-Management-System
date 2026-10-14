from django.urls import path

from .views import VisitorCollectionView, VisitorExitView


urlpatterns = [
    path("visitors", VisitorCollectionView.as_view(), name="visitor-list-create"),
    path("visitors/<int:visitor_id>/exit", VisitorExitView.as_view(), name="visitor-exit"),
]
