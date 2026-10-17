from django.urls import include, path


urlpatterns = [
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/", include("visitors.urls")),
    path("api/v1/", include("mess.urls")),
    path("api/v1/", include("leave_requests.urls")),
]
