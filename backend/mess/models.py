from django.core.exceptions import ValidationError
from django.db import models


class WeeklyMenu(models.Model):
    week_start = models.DateField(unique=True)
    menu = models.JSONField()
    published_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-week_start",)

    def clean(self):
        if not isinstance(self.menu, dict) or not self.menu:
            raise ValidationError({"menu": "Provide a non-empty JSON object for the weekly menu."})

    def __str__(self):
        return f"Weekly mess menu starting {self.week_start.isoformat()}"
