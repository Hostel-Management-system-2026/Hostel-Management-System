from django.db import migrations, models

class Migration(migrations.Migration):

```
initial = True

dependencies = []

operations = [
    migrations.CreateModel(
        name="StudentProfile",
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
            (
                "user_id",
                models.CharField(
                    db_index=True,
                    max_length=64,
                    unique=True,
                ),
            ),
            (
                "student_number",
                models.CharField(max_length=64, unique=True),
            ),
            ("full_name", models.CharField(max_length=160)),
            ("email", models.EmailField(blank=True, max_length=254)),
            ("phone", models.CharField(blank=True, max_length=32)),
            ("room_number", models.CharField(blank=True, max_length=32)),
            ("course", models.CharField(blank=True, max_length=120)),
            (
                "year_of_study",
                models.PositiveSmallIntegerField(blank=True, null=True),
            ),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ],
        options={
            "ordering": ("student_number",),
        },
    ),
]
```
