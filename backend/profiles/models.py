from django.db import models


class StudentProfile(models.Model):
    # Account ID from the existing authentication layer.
    user_id = models.CharField(max_length=64, unique=True, db_index=True)
    student_number = models.CharField(max_length=64, unique=True)
    full_name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    room_number = models.CharField(max_length=32, blank=True)
    course = models.CharField(max_length=120, blank=True)
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("student_number",)

    def __str__(self):
        return f"{self.student_number} - {self.full_name}"
