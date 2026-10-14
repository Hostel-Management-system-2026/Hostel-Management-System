from django.db import migrations, models

class Migration(migrations.Migration):
initial = True

```
dependencies = []

operations = [
    migrations.CreateModel(
        name="Notice",
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
            ("title", models.CharField(max_length=180)),
            ("body", models.TextField(max_length=10000)),
            (
                "audience",
                models.CharField(
                    default="ALL_STUDENTS",
                    max_length=80,
                ),
            ),
            ("is_published", models.BooleanField(default=True)),
            ("published_by", models.CharField(max_length=64)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ],
        options={
            "ordering": ("-created_at",),
        },
    ),
]
```
