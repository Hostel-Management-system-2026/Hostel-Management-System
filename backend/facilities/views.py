
from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsStudent, IsWardenOrAdmin
from .models import Facility, FacilityBooking
from .serializers import FacilitySerializer, FacilityBookingSerializer


class FacilityListView(generics.ListAPIView):
    """Allow students to view active facilities."""

    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Facility.objects.filter(is_active=True)


class FacilityAvailabilityView(APIView):
    """Show confirmed bookings for a facility on a selected date."""

    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, facility_id):
        booking_date = request.query_params.get("date")

        if not booking_date:
            raise ValidationError({"date": "This query parameter is required."})

        try:
            facility = Facility.objects.get(
                id=facility_id,
                is_active=True,
            )
        except Facility.DoesNotExist:
            return Response(
                {"detail": "Facility not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        bookings = FacilityBooking.objects.filter(
            facility=facility,
            booking_date=booking_date,
            status=FacilityBooking.Status.CONFIRMED,
        ).order_by("start_time")

        return Response({
            "facility": FacilitySerializer(facility).data,
            "date": booking_date,
            "booked_slots": FacilityBookingSerializer(
                bookings,
                many=True,
            ).data,
        })


class FacilityBookingCreateView(APIView):
    """Create a booking while preventing overlapping reservations."""

    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        serializer = FacilityBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        facility_id = serializer.validated_data["facility"].id
        booking_date = serializer.validated_data["booking_date"]
        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]

        with transaction.atomic():
            try:
                facility = Facility.objects.select_for_update().get(
                    id=facility_id,
                    is_active=True,
                )
            except Facility.DoesNotExist:
                return Response(
                    {"detail": "Facility not found or inactive."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            conflicting_booking = FacilityBooking.objects.filter(
                facility=facility,
                booking_date=booking_date,
                status=FacilityBooking.Status.CONFIRMED,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if conflicting_booking:
                return Response(
                    {"detail": "This facility slot is already booked."},
                    status=status.HTTP_409_CONFLICT,
                )

            booking = FacilityBooking.objects.create(
                facility=facility,
                student=request.user,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
            )

        return Response(
            FacilityBookingSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )
        
class StaffFacilityListCreateView(generics.ListCreateAPIView):
    """Allow wardens and admins to list and create facilities."""

    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated, IsWardenOrAdmin]


class StaffFacilityDetailView(generics.RetrieveUpdateAPIView):
    """Allow wardens and admins to view and update facilities."""

    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated, IsWardenOrAdmin]        