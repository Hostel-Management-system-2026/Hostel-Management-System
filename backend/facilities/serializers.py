from rest_framework import serializers

from .models import Facility, FacilityBooking

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            "id",
            "name",
            "description",
            "location",
            "capacity",
            "is_active",
        ]


class FacilityBookingSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source="student.username")
    facility_name = serializers.ReadOnlyField(source="facility.name")

    class Meta:
        model = FacilityBooking
        fields = [
            "id",
            "facility",
            "facility_name",
            "student",
            "booking_date",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, attrs):
        if attrs["end_time"] <= attrs["start_time"]:
            raise serializers.ValidationError(
                "End time must be later than start time."
            )
        return attrs