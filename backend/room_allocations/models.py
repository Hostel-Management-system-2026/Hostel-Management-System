from django.conf import settings
from django.db import models


class Room(models.Model):
    room_number = models.CharField(max_length=32, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class RoomAllocation(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="room_allocations",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="allocations",
    )
    allocated_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student"],
                condition=models.Q(released_at__isnull=True),
                name="one_active_room_per_student",
            ),
            models.UniqueConstraint(
                fields=["room"],
                condition=models.Q(released_at__isnull=True),
                name="one_active_allocation_per_room",
            ),
        ]

    def __str__(self):
        return f"{self.student} - {self.room}"