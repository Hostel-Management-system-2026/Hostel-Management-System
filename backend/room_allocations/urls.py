from django.urls import path

from .views import RoomAllocationListCreateView

urlpatterns = [
    path("allocations/", RoomAllocationListCreateView.as_view(), name="room-allocation-list-create"),
]