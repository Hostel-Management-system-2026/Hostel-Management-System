from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdmin, IsStudent
from .models import StudentProfile
from .serializers import StudentProfileSerializer


class MyStudentProfileView(APIView):
    permission_classes = (IsStudent,)

    def get(self, request):
        profile = get_object_or_404(StudentProfile, user_id=str(request.user.pk))
        return Response(StudentProfileSerializer(profile).data)

    def put(self, request):
        raise PermissionDenied("Students have read-only access to their profile.")

    def patch(self, request):
        raise PermissionDenied("Students have read-only access to their profile.")

    def delete(self, request):
        raise PermissionDenied("Students cannot delete their profile.")


class StudentProfileCollectionView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        profiles = StudentProfile.objects.all()
        return Response(StudentProfileSerializer(profiles, many=True).data)

    def post(self, request):
        serializer = StudentProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(StudentProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


class StudentProfileDetailView(APIView):
    permission_classes = (IsAdmin,)

    def get_object(self, profile_id):
        return get_object_or_404(StudentProfile, pk=profile_id)

    def get(self, request, profile_id):
        return Response(StudentProfileSerializer(self.get_object(profile_id)).data)

    def patch(self, request, profile_id):
        profile = self.get_object(profile_id)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, profile_id):
        profile = self.get_object(profile_id)
        serializer = StudentProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, profile_id):
        self.get_object(profile_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
