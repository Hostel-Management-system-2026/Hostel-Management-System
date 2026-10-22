from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin
from .models import Room, RoomAllocation
from .serializers import RoomAllocationSerializer


class RoomInventoryView(generics.ListAPIView):
    """List room capacity and occupancy for the admin allocation workspace."""
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Room.objects.annotate(
            active_allocations=Count("allocations", filter=Q(allocations__released_at__isnull=True)),
        ).order_by("room_number")

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        data = []
        for room in rooms:
            occupied = room.active_allocations
            data.append({
                "id": room.pk,
                "room_number": room.room_number,
                "capacity": room.capacity,
                "is_available": room.is_available,
                "occupied": occupied,
                "available_beds": max(room.capacity - occupied, 0),
            })
        return Response(data)


class RoomAllocationListCreateView(generics.ListCreateAPIView):
    queryset = RoomAllocation.objects.select_related("student", "room").all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AllocationConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This room allocation has already been released."
    default_code = "allocation_already_released"


class RoomAllocationReleaseView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, allocation_id):
        with transaction.atomic():
            allocation = get_object_or_404(RoomAllocation.objects.select_for_update(), pk=allocation_id)
            if allocation.released_at is not None:
                raise AllocationConflict()
            allocation.released_at = timezone.now()
            allocation.save(update_fields=("released_at",))
        return Response(RoomAllocationSerializer(allocation).data)
