from django.urls import path

from .views import RoomAllocationListCreateView, RoomAllocationReleaseView, RoomInventoryView

urlpatterns = [
    path("rooms/", RoomInventoryView.as_view(), name="room-inventory"),
    path("allocations/", RoomAllocationListCreateView.as_view(), name="room-allocation-list-create"),
    path("allocations/<int:allocation_id>/release", RoomAllocationReleaseView.as_view(), name="room-allocation-release"),
]
