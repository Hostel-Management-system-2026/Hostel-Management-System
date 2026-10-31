
from django.contrib import admin

from .models import Facility, FacilityBooking


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "capacity", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")
    ordering = ("name",)


@admin.register(FacilityBooking)
class FacilityBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "facility",
        "student",
        "booking_date",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "booking_date")
    search_fields = ("facility__name", "student__username")
    ordering = ("-booking_date", "start_time")
    readonly_fields = ("created_at",)
