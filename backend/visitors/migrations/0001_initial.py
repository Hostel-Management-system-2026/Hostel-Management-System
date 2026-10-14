from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VisitorLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("visitor_name", models.CharField(max_length=160)),
                ("student_id", models.CharField(max_length=64)),
                ("room_number", models.CharField(max_length=32)),
                ("purpose", models.CharField(blank=True, max_length=240)),
                ("entry_at", models.DateTimeField()),
                ("exit_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-entry_at",)},
        ),
    ]
