from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeeklyMenu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_start", models.DateField(unique=True)),
                ("menu", models.JSONField()),
                ("published_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("-week_start",)},
        ),
    ]
