from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=180)
    body = models.TextField(max_length=10000)
    audience = models.CharField(max_length=80, default="ALL_STUDENTS")
    is_published = models.BooleanField(default=True)
    published_by = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} ({'published' if self.is_published else 'draft'})"
