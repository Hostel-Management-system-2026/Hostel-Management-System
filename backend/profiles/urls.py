from django.urls import path

from .views import MyStudentProfileView, StudentProfileCollectionView, StudentProfileDetailView

urlpatterns = [
    path("profiles/me", MyStudentProfileView.as_view(), name="my-student-profile"),
    path("profiles", StudentProfileCollectionView.as_view(), name="student-profile-list-create"),
    path("profiles/<int:profile_id>", StudentProfileDetailView.as_view(), name="student-profile-detail"),
]
