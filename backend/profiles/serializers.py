from rest_framework import serializers

from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = (
            "id", "user_id", "student_number", "full_name", "email", "phone",
            "room_number", "course", "year_of_study", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_student_number(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Student number is required.")
        return value

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value
