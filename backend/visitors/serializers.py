from rest_framework import serializers

from .models import VisitorLog


class VisitorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorLog
        fields = (
            "id",
            "visitor_name",
            "student_id",
            "room_number",
            "purpose",
            "entry_at",
            "exit_at",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        entry_at = attrs.get("entry_at", getattr(self.instance, "entry_at", None))
        exit_at = attrs.get("exit_at", getattr(self.instance, "exit_at", None))
        if exit_at and entry_at and exit_at < entry_at:
            raise serializers.ValidationError({"exit_at": "Exit time cannot be earlier than entry time."})
        return attrs
