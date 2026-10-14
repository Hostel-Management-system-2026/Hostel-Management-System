from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="leave_requests",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=2000)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="decided_leave_requests",
    )
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-submitted_at",)

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be before start date."})

    def __str__(self):
        return f"Leave request {self.pk} for user {self.student_id}: {self.status}"
