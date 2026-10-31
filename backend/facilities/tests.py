
from datetime import date, time

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Facility, FacilityBooking


User = get_user_model()


class FacilityBookingTests(APITestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password="Test@12345",
            role="STUDENT",
        )

        self.other_student = User.objects.create_user(
            username="student2",
            password="Test@12345",
            role="STUDENT",
        )

        self.warden = User.objects.create_user(
            username="warden1",
            password="Test@12345",
            role="WARDEN",
        )

        self.facility = Facility.objects.create(
            name="Badminton Court",
            description="Indoor badminton court",
            location="Block A",
            capacity=4,
            is_active=True,
        )

        self.booking_url = "/api/v1/facility-bookings/"
        self.availability_url = (
            f"/api/v1/facilities/{self.facility.id}/availability/"
        )

        self.booking_data = {
            "facility": self.facility.id,
            "booking_date": "2026-11-01",
            "start_time": "16:00:00",
            "end_time": "17:00:00",
        }

    def test_student_can_view_facilities(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.get("/api/v1/facilities/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_book_available_slot(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            self.booking_url,
            self.booking_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FacilityBooking.objects.count(), 1)

    def test_overlapping_booking_is_rejected(self):
        self.client.force_authenticate(user=self.student)

        first_response = self.client.post(
            self.booking_url,
            self.booking_data,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_data = {
            **self.booking_data,
            "start_time": "16:30:00",
            "end_time": "17:30:00",
        }

        second_response = self.client.post(
            self.booking_url,
            second_data,
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(FacilityBooking.objects.count(), 1)

        original_booking = FacilityBooking.objects.get()

        self.assertEqual(original_booking.student, self.student)
        self.assertEqual(original_booking.start_time, time(16, 0))
        self.assertEqual(original_booking.end_time, time(17, 0))
        self.assertEqual(
            original_booking.status,
            FacilityBooking.Status.CONFIRMED,
        )

    def test_adjacent_bookings_are_allowed(self):
        self.client.force_authenticate(user=self.student)

        self.client.post(
            self.booking_url,
            self.booking_data,
            format="json",
        )

        adjacent_data = {
            **self.booking_data,
            "start_time": "17:00:00",
            "end_time": "18:00:00",
        }

        response = self.client.post(
            self.booking_url,
            adjacent_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FacilityBooking.objects.count(), 2)

    def test_availability_shows_existing_bookings(self):
        FacilityBooking.objects.create(
            facility=self.facility,
            student=self.student,
            booking_date=date(2026, 11, 1),
            start_time=time(16, 0),
            end_time=time(17, 0),
        )

        self.client.force_authenticate(user=self.other_student)

        response = self.client.get(
            self.availability_url,
            {"date": "2026-11-01"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["booked_slots"]), 1)

    def test_warden_cannot_access_student_booking_api(self):
        self.client.force_authenticate(user=self.warden)

        response = self.client.get("/api/v1/facilities/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_view_facilities(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/v1/facilities/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class StaffFacilityManagementTests(APITestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username="staff_test_student",
            password="Test@12345",
            role="STUDENT",
        )

        self.warden = User.objects.create_user(
            username="staff_test_warden",
            password="Test@12345",
            role="WARDEN",
        )

        self.admin = User.objects.create_user(
            username="staff_test_admin",
            password="Test@12345",
            role="ADMIN",
        )

        self.list_url = "/api/v1/staff/facilities/"

        self.facility_data = {
            "name": "Swimming Pool",
            "description": "Indoor swimming pool",
            "location": "Block B",
            "capacity": 30,
            "is_active": True,
        }

    def test_warden_can_create_facility(self):
        self.client.force_authenticate(user=self.warden)

        response = self.client.post(
            self.list_url,
            self.facility_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Facility.objects.filter(name="Swimming Pool").exists()
        )

    def test_admin_can_create_facility(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.list_url,
            self.facility_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_warden_can_list_facilities(self):
        Facility.objects.create(**self.facility_data)
        self.client.force_authenticate(user=self.warden)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_warden_can_update_facility(self):
        facility = Facility.objects.create(**self.facility_data)
        self.client.force_authenticate(user=self.warden)

        response = self.client.patch(
            f"{self.list_url}{facility.id}/",
            {"capacity": 40},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        facility.refresh_from_db()
        self.assertEqual(facility.capacity, 40)

    def test_student_cannot_access_staff_facility_api(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_access_staff_facility_api(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
