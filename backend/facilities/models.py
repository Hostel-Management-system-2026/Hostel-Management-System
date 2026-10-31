
from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FacilityBooking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="facility_bookings",
    )
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "start_time"]
        constraints = [
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="facility_booking_valid_time_range",
            ),
        ]
        indexes = [
            models.Index(
                fields=["facility", "booking_date", "status"],
                name="facility_booking_lookup_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.facility.name} - {self.booking_date} "
            f"({self.start_time}-{self.end_time})"
        )
