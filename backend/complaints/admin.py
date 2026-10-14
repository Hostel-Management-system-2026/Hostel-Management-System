from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "student_id", "status", "created_at")
    search_fields = ("title", "student_id", "description")
    list_filter = ("status", "created_at")
