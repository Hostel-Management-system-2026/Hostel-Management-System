from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = (
            "id", "title", "body", "audience", "is_published",
            "published_by", "created_at", "updated_at",
        )
        read_only_fields = ("id", "published_by", "created_at", "updated_at")

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Notice title is required.")
        return value

    def validate_body(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Notice body is required.")
        return value
