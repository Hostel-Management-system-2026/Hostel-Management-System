from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsStudent, IsStudentOrWarden, IsWarden
from .models import Complaint
from .serializers import ComplaintSerializer


class InvalidTransition(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Invalid status transition. Allowed sequence: OPEN -> IN_PROGRESS -> RESOLVED."
    default_code = "invalid_complaint_transition"


class ComplaintCollectionView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStudent()]
        return [IsStudentOrWarden()]

    def get(self, request):
        complaints = Complaint.objects.all()
        if IsStudent().has_permission(request, self):
            complaints = complaints.filter(student_id=str(request.user.pk))
        return Response(ComplaintSerializer(complaints, many=True).data)

    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        complaint = serializer.save(student_id=str(request.user.pk), status=Complaint.Status.OPEN)
        return Response(ComplaintSerializer(complaint).data, status=status.HTTP_201_CREATED)


class ComplaintDetailView(APIView):
    permission_classes = (IsWarden,)

    def patch(self, request, complaint_id):
        next_status = request.data.get("status")
        if not isinstance(next_status, str):
            raise ValidationError({"status": "A valid next status is required."})
        next_status = next_status.upper()
        allowed = {
            Complaint.Status.OPEN: Complaint.Status.IN_PROGRESS,
            Complaint.Status.IN_PROGRESS: Complaint.Status.RESOLVED,
        }
        with transaction.atomic():
            complaint = get_object_or_404(Complaint.objects.select_for_update(), pk=complaint_id)
            if allowed.get(complaint.status) != next_status:
                raise InvalidTransition()
            complaint.status = next_status
            complaint.save(update_fields=("status", "updated_at"))
        return Response(ComplaintSerializer(complaint).data)
