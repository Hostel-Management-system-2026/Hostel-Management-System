from rest_framework import serializers

from .models import WeeklyMenu

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MEALS = ("breakfast", "lunch", "dinner")


class WeeklyMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyMenu
        fields = ("id", "week_start", "menu", "published_at")
        read_only_fields = ("id", "published_at")

    def validate_menu(self, value):
        if not isinstance(value, dict) or set(value) != {"days"}:
            raise serializers.ValidationError("Menu must contain a 'days' object with all seven weekdays.")

        days = value["days"]
        if not isinstance(days, dict) or set(days) != set(WEEKDAYS):
            raise serializers.ValidationError("Provide menu data for Monday through Sunday.")

        for day in WEEKDAYS:
            meals = days[day]
            if not isinstance(meals, dict) or set(meals) != set(MEALS):
                raise serializers.ValidationError(
                    f"{day} must contain breakfast, lunch, and dinner item lists."
                )
            for meal in MEALS:
                items = meals[meal]
                if (
                    not isinstance(items, list)
                    or not items
                    or any(not isinstance(item, str) or not item.strip() for item in items)
                ):
                    raise serializers.ValidationError(
                        f"{day} {meal} must be a non-empty list of menu item names."
                    )
        return value
