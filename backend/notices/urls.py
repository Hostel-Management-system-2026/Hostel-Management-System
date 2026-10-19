from django.urls import path

from .views import NoticeCollectionView, NoticeDetailView

urlpatterns = [
    path("notices", NoticeCollectionView.as_view(), name="notice-list-create"),
    path("notices/<int:notice_id>", NoticeDetailView.as_view(), name="notice-detail"),
]
