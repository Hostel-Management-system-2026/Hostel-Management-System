from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin
from .models import RoomAllocation
from .serializers import RoomAllocationSerializer


class RoomAllocationListCreateView(generics.ListCreateAPIView):
    queryset = RoomAllocation.objects.select_related("student", "room").all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]