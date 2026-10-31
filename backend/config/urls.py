from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/", include("room_allocations.urls")),
    path("api/v1/", include("profiles.urls")),
    path("api/v1/", include("complaints.urls")),
    path("api/v1/", include("facilities.urls")),
    path("api/v1/", include("fees.urls")),
    path("api/v1/", include("leave_requests.urls")),
    path("api/v1/", include("mess.urls")),
    path("api/v1/", include("notices.urls")),
    path("api/v1/", include("visitors.urls")),
]