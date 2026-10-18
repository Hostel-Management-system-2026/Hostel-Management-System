from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Room, RoomAllocation

User = get_user_model()


class RoomAllocationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin",
            password="TestPass123!",
            role="ADMIN",
        )
        self.student = User.objects.create_user(
            username="student",
            password="TestPass123!",
            role="STUDENT",
        )
        self.other_student = User.objects.create_user(
            username="student2",
            password="TestPass123!",
            role="STUDENT",
        )
        self.room = Room.objects.create(
            room_number="A-101",
            capacity=1,
            is_available=True,
        )
        self.url = "/api/v1/allocations/"

    def test_admin_can_allocate_available_room(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.pk,
                "room_id": self.room.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            RoomAllocation.objects.filter(
                student=self.student,
                room=self.room,
                released_at__isnull=True,
            ).exists()
        )

    def test_student_cannot_allocate_room(self):
        self.client.force_authenticate(self.student)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.pk,
                "room_id": self.room.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(RoomAllocation.objects.count(), 0)

    def test_student_cannot_have_two_active_allocations(self):
        RoomAllocation.objects.create(
            student=self.student,
            room=self.room,
        )
        second_room = Room.objects.create(
            room_number="A-102",
            capacity=1,
            is_available=True,
        )
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.pk,
                "room_id": second_room.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_room_cannot_be_allocated_twice(self):
        RoomAllocation.objects.create(
            student=self.student,
            room=self.room,
        )
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {
                "student_id": self.other_student.pk,
                "room_id": self.room.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_user_cannot_allocate_room(self):
        response = self.client.post(
            self.url,
            {
                "student_id": self.student.pk,
                "room_id": self.room.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(RoomAllocation.objects.count(), 0)