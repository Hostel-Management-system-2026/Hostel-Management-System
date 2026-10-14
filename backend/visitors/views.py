from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError
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

        class ExitTimestampSerializer(serializers.Serializer):
            exit_at = serializers.DateTimeField(required=False)

        serializer = ExitTimestampSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exit_at = serializer.validated_data.get("exit_at", timezone.now())
        if exit_at < record.entry_at:
            raise ValidationError({"exit_at": "Exit time cannot be earlier than entry time."})

        # The conditional update is the concurrency guard: only one request can
        # change a still-open visit, even when requests arrive at the same time.
        with transaction.atomic():
            updated = VisitorLog.objects.filter(pk=visitor_id, exit_at__isnull=True).update(exit_at=exit_at)
        if updated == 0:
            if not VisitorLog.objects.filter(pk=visitor_id).exists():
                raise Http404
            raise Conflict()

        record.refresh_from_db(fields=("exit_at",))
        return Response(VisitorLogSerializer(record).data)
