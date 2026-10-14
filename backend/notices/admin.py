from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "is_published", "published_by", "created_at")
    search_fields = ("title", "body")
    list_filter = ("is_published", "audience", "created_at")
