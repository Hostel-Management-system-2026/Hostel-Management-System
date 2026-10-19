
from rest_framework import serializers

from accounts.models import User
from .models import Room, RoomAllocation


class RoomAllocationSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.STUDENT),
        source="student",
        write_only=True,
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source="room",
        write_only=True,
    )

    class Meta:
        model = RoomAllocation
        fields = [
            "id",
            "student_id",
            "room_id",
            "allocated_at",
            "released_at",
        ]
        read_only_fields = ["id", "allocated_at", "released_at"]

    def validate(self, attrs):
        student = attrs["student"]
        room = attrs["room"]

        # A student can have only one active room allocation.
        if RoomAllocation.objects.filter(
            student=student,
            released_at__isnull=True,
        ).exists():
            raise serializers.ValidationError(
                {
                    "student_id": (
                        "This student already has an active allocation."
                    )
                }
            )

        # Reject rooms marked as unavailable.
        if not room.is_available:
            raise serializers.ValidationError(
                {"room_id": "This room is not available."}
            )

        # Allow multiple students, up to the room's capacity.
        active_allocations = RoomAllocation.objects.filter(
            room=room,
            released_at__isnull=True,
        ).count()

        if active_allocations >= room.capacity:
            raise serializers.ValidationError(
                {"room_id": "This room has reached its capacity."}
            )

        return attrs
