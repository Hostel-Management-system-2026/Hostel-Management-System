from rest_framework import serializers

from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField(source="student.pk")
    decided_by = serializers.ReadOnlyField(source="decided_by.pk", allow_null=True)

    class Meta:
        model = LeaveRequest
        fields = (
            "id",
            "student_id",
            "start_date",
            "end_date",
            "reason",
            "status",
            "submitted_at",
            "decided_by",
            "decided_at",
        )
        read_only_fields = ("id", "student_id", "status", "submitted_at", "decided_by", "decided_at")

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})
        return attrs

    def validate_reason(self, value):
        if not value.strip():
            raise serializers.ValidationError("A reason is required.")
        return value.strip()
