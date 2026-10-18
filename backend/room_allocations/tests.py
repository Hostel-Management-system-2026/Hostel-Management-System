
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
        self.third_student = User.objects.create_user(
            username="student3",
            password="TestPass123!",
            role="STUDENT",
        )
        self.fourth_student = User.objects.create_user(
            username="student4",
            password="TestPass123!",
            role="STUDENT",
        )

        self.room = Room.objects.create(
            room_number="A-101",
            capacity=1,
            is_available=True,
        )
        self.url = "/api/v1/allocations/"

    def allocate(self, student, room=None):
        return self.client.post(
            self.url,
            {
                "student_id": student.pk,
                "room_id": (room or self.room).pk,
            },
            format="json",
        )

    def test_admin_can_allocate_available_room(self):
        self.client.force_authenticate(self.admin)

        response = self.allocate(self.student)

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

        response = self.allocate(self.student)

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

        response = self.allocate(self.student, second_room)

        self.assertEqual(response.status_code, 400)

    def test_room_capacity_one_rejects_second_student(self):
        RoomAllocation.objects.create(
            student=self.student,
            room=self.room,
        )
        self.client.force_authenticate(self.admin)

        response = self.allocate(self.other_student)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            RoomAllocation.objects.filter(
                room=self.room,
                released_at__isnull=True,
            ).count(),
            1,
        )

    def test_room_capacity_three_accepts_three_students(self):
        shared_room = Room.objects.create(
            room_number="B-301",
            capacity=3,
            is_available=True,
        )
        self.client.force_authenticate(self.admin)

        for student in (
            self.student,
            self.other_student,
            self.third_student,
        ):
            response = self.allocate(student, shared_room)
            self.assertEqual(response.status_code, 201)

        self.assertEqual(
            RoomAllocation.objects.filter(
                room=shared_room,
                released_at__isnull=True,
            ).count(),
            3,
        )

    def test_room_capacity_three_rejects_fourth_student(self):
        shared_room = Room.objects.create(
            room_number="B-302",
            capacity=3,
            is_available=True,
        )
        RoomAllocation.objects.create(
            student=self.student,
            room=shared_room,
        )
        RoomAllocation.objects.create(
            student=self.other_student,
            room=shared_room,
        )
        RoomAllocation.objects.create(
            student=self.third_student,
            room=shared_room,
        )
        self.client.force_authenticate(self.admin)

        response = self.allocate(self.fourth_student, shared_room)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            RoomAllocation.objects.filter(
                room=shared_room,
                released_at__isnull=True,
            ).count(),
            3,
        )

    def test_unavailable_room_is_rejected(self):
        unavailable_room = Room.objects.create(
            room_number="C-101",
            capacity=3,
            is_available=False,
        )
        self.client.force_authenticate(self.admin)

        response = self.allocate(self.student, unavailable_room)

        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_user_cannot_allocate_room(self):
        response = self.allocate(self.student)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(RoomAllocation.objects.count(), 0)
