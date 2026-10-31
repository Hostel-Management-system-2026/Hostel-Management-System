
from django.urls import path

from .views import (
    FacilityListView,
    FacilityAvailabilityView,
    FacilityBookingCreateView,
)

urlpatterns = [
    path("facilities/", FacilityListView.as_view(), name="facility-list"),
    path(
        "facilities/<int:facility_id>/availability/",
        FacilityAvailabilityView.as_view(),
        name="facility-availability",
    ),
    path(
        "facility-bookings/",
        FacilityBookingCreateView.as_view(),
        name="facility-booking-create",
    ),
]
