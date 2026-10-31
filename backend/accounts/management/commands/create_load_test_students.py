
import csv
import secrets
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from profiles.models import StudentProfile


class Command(BaseCommand):
    help = "Create synthetic student accounts for local load testing."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=500)
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm creation of synthetic load-test accounts.",
        )

    def handle(self, *args, **options):
        count = options["count"]

        if not options["confirm"]:
            raise CommandError(
                "Use --confirm to create synthetic test accounts."
            )

        if count < 1 or count > 500:
            raise CommandError("Count must be between 1 and 500.")

        if connection.vendor != "sqlite":
            raise CommandError(
                "This command is restricted to SQLite local development."
            )

        User = get_user_model()
        credentials = []

        csv_path = (
            Path(settings.BASE_DIR).parent
            / "load_tests"
            / "data"
            / "students.csv"
        )
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        with transaction.atomic():
            for number in range(1, count + 1):
                username = f"loadtest_{number:04d}"
                password = secrets.token_urlsafe(18)

                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "email": f"{username}@example.test",
                        "role": "STUDENT",
                        "is_active": True,
                    },
                )

                # These usernames are reserved for this local test command.
                user.role = "STUDENT"
                user.is_active = True
                user.set_password(password)
                user.save()

                StudentProfile.objects.get_or_create(
                    user_id=str(user.pk),
                    defaults={
                        "student_number": f"LT{number:05d}",
                        "full_name": f"Load Test Student {number:04d}",
                        "email": f"{username}@example.test",
                        "course": "Computer Science",
                        "year_of_study": 2,
                    },
                )

                credentials.append((username, password))

                action = "Created" if created else "Updated"
                self.stdout.write(f"{action}: {username}")

        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])
            writer.writerows(credentials)

        self.stdout.write(
            self.style.SUCCESS(
                f"Prepared {count} synthetic students. "
                f"Credentials saved to {csv_path}"
            )
        )
