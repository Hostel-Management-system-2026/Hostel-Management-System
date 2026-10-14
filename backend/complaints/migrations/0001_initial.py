from django.db import migrations, models

class Migration(migrations.Migration):
initial = True

```
dependencies = []

operations = [
    migrations.CreateModel(
        name="Complaint",
        fields=[
            (
                "id",
                models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID",
                ),
            ),
            ("student_id", models.CharField(db_index=True, max_length=64)),
            ("title", models.CharField(max_length=160)),
            ("description", models.TextField(max_length=4000)),
            (
                "status",
                models.CharField(
                    choices=[
                        ("OPEN", "Open"),
                        ("IN_PROGRESS", "In Progress"),
                        ("RESOLVED", "Resolved"),
                    ],
                    default="OPEN",
                    max_length=16,
                ),
            ),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ],
        options={
            "ordering": ("-created_at",),
        },
    ),
]
```
