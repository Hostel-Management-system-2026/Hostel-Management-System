from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsWarden
from .models import VisitorLog
from .serializers import VisitorLogSerializer


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This visitor log has already been closed."
    default_code = "visitor_log_closed"


class VisitorCollectionView(APIView):
    permission_classes = (IsWarden,)

    def post(self, request):
        serializer = VisitorLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response(VisitorLogSerializer(record).data, status=status.HTTP_201_CREATED)


class VisitorExitView(APIView):
    permission_classes = (IsWarden,)

    def patch(self, request, visitor_id):
        record = get_object_or_404(VisitorLog, pk=visitor_id)
        if record.exit_at is not None:
            raise Conflict()

        requested_exit = request.data.get("exit_at")
        if requested_exit is None:
            record.exit_at = timezone.now()
        else:
            serializer = VisitorLogSerializer(
                record,
                data={"exit_at": requested_exit},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            record.exit_at = serializer.validated_data["exit_at"]

        record.full_clean()
        record.save(update_fields=("exit_at",))
        return Response(VisitorLogSerializer(record).data)
