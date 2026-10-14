from rest_framework import serializers

from .models import WeeklyMenu


class WeeklyMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyMenu
        fields = ("id", "week_start", "menu", "published_at")
        read_only_fields = ("id", "published_at")

    def validate_menu(self, value):
        if not isinstance(value, dict) or not value:
            raise serializers.ValidationError("Provide a non-empty JSON object for the weekly menu.")
        return value
