from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student_number", "full_name", "user_id", "room_number", "course")
    search_fields = ("student_number", "full_name", "user_id", "email")
    list_filter = ("course", "year_of_study")
