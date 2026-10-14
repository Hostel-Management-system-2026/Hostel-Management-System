from django.core.exceptions import ValidationError
from django.db import models


class VisitorLog(models.Model):
    visitor_name = models.CharField(max_length=160)
    student_id = models.CharField(max_length=64)
    room_number = models.CharField(max_length=32)
    purpose = models.CharField(max_length=240, blank=True)
    entry_at = models.DateTimeField()
    exit_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-entry_at",)

    def clean(self):
        if self.exit_at and self.entry_at and self.exit_at < self.entry_at:
            raise ValidationError({"exit_at": "Exit time cannot be earlier than entry time."})

    def __str__(self):
        return f"{self.visitor_name} visiting {self.student_id} ({self.entry_at.isoformat()})"
