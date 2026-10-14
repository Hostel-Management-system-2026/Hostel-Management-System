from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdmin, IsStudentOrWardenOrAdmin
from .models import WeeklyMenu
from .serializers import WeeklyMenuSerializer


class WeeklyMenuView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsStudentOrWardenOrAdmin()]

    def get(self, request):
        menu = WeeklyMenu.objects.first()
        if menu is None:
            raise NotFound("No weekly mess menu has been published yet.")
        return Response(WeeklyMenuSerializer(menu).data)

    def post(self, request):
        serializer = WeeklyMenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        week_start = serializer.validated_data["week_start"]
        menu, created = WeeklyMenu.objects.update_or_create(
            week_start=week_start,
            defaults={"menu": serializer.validated_data["menu"]},
        )
        result = WeeklyMenuSerializer(menu).data
        return Response(result, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
