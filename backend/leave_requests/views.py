from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsStudent, IsStudentOrWarden, IsWarden
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Only pending leave requests can receive a decision."
    default_code = "leave_request_already_decided"


class LeaveRequestCollectionView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStudent()]
        return [IsStudentOrWarden()]

    def get(self, request):
        requests = LeaveRequest.objects.all()
        if IsStudent().has_permission(request, self):
            requests = requests.filter(student=request.user)
        return Response(LeaveRequestSerializer(requests, many=True).data)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        leave_request = serializer.save(
            student=request.user,
            status=LeaveRequest.Status.PENDING,
        )
        return Response(LeaveRequestSerializer(leave_request).data, status=status.HTTP_201_CREATED)


class LeaveDecisionView(APIView):
    permission_classes = (IsWarden,)

    def patch(self, request, leave_id):
        decision = request.data.get("decision")
        if not isinstance(decision, str) or decision.upper() not in {"APPROVE", "REJECT"}:
            raise ValidationError({"decision": "Use 'approve' or 'reject'."})

        with transaction.atomic():
            leave_request = get_object_or_404(LeaveRequest.objects.select_for_update(), pk=leave_id)
            if leave_request.status != LeaveRequest.Status.PENDING:
                raise Conflict()

            leave_request.status = (
                LeaveRequest.Status.APPROVED
                if decision.upper() == "APPROVE"
                else LeaveRequest.Status.REJECTED
            )
            leave_request.decided_by = request.user
            leave_request.decided_at = timezone.now()
            leave_request.save(update_fields=("status", "decided_by", "decided_at"))

        return Response(LeaveRequestSerializer(leave_request).data)
