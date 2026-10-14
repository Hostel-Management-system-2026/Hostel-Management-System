from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdmin, IsStudent
from .models import Notice
from .serializers import NoticeSerializer


class NoticeCollectionView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        # GET is restricted to students or admins; role-specific branch below checks access.
        from rest_framework.permissions import IsAuthenticated
        return [IsAuthenticated()]

    def get(self, request):
        role = str(getattr(request.user, "role", "") or "").upper().removeprefix("ROLE_")
        token = request.auth
        if not role and token is not None:
            role = str(token.get("role", "") if isinstance(token, dict) else getattr(token, "role", "")).upper().removeprefix("ROLE_")
        if role == "ADMIN":
            notices = Notice.objects.all()
        elif role == "STUDENT":
            notices = Notice.objects.filter(is_published=True, audience__in=("ALL_STUDENTS", "STUDENTS"))
        else:
            raise PermissionDenied("Only students and admins can view notices.")
        return Response(NoticeSerializer(notices, many=True).data)

    def post(self, request):
        serializer = NoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notice = serializer.save(published_by=str(request.user.pk))
        return Response(NoticeSerializer(notice).data, status=status.HTTP_201_CREATED)


class NoticeDetailView(APIView):
    def get_permissions(self):
        from rest_framework.permissions import IsAuthenticated
        return [IsAuthenticated()]

    def get(self, request, notice_id):
        notice = get_object_or_404(Notice, pk=notice_id)
        role = str(getattr(request.user, "role", "") or "").upper().removeprefix("ROLE_")
        token = request.auth
        if not role and token is not None:
            role = str(token.get("role", "") if isinstance(token, dict) else getattr(token, "role", "")).upper().removeprefix("ROLE_")
        if role != "ADMIN" and not (role == "STUDENT" and notice.is_published and notice.audience in ("ALL_STUDENTS", "STUDENTS")):
            raise PermissionDenied("You cannot view this notice.")
        return Response(NoticeSerializer(notice).data)

    def patch(self, request, notice_id):
        if not IsAdmin().has_permission(request, self):
            raise PermissionDenied("Only admins can update notices.")
        notice = get_object_or_404(Notice, pk=notice_id)
        serializer = NoticeSerializer(notice, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, notice_id):
        if not IsAdmin().has_permission(request, self):
            raise PermissionDenied("Only admins can delete notices.")
        get_object_or_404(Notice, pk=notice_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
