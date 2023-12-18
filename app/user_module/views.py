from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from app.user_module.models import (
    AddressInfo,
    AssociationsInfo,
    CertificationsInfo,
    EducationInfo,
    PersonalInfo,
    ProfileInfo,
    SkillsInfo,
    SocialMediaInfo,
    WorkExperienceInfo,
)

from .filters import UserInsightFilter
from .serializers import (
    AddressInfoSerializer,
    AssociationsInfoSerializer,
    CertificationsInfoSerializer,
    EducationInfoSerializer,
    PersonalInfoSerializer,
    ProfileInfoSerializer,
    SkillsInfoSerializer,
    SocialMediaInfoSerializer,
    UserSerializer,
    WorkExperienceInfoSerializer,
)

# from app.caching_mixins import CacheMixin

User = get_user_model()


class CustomUserCreateView(CreateAPIView):
    """
    check whether the user input 'PF' or 'scholar_code' exists in UserData table before creating a new user
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    """
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    """


class CustomUserListView(ListAPIView):
    """
    View to list all users.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class FindUserView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInsightFilter

    # @CacheMixin.cache_view
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateAPIView):

    """
     # (RetrieveUpdateDestroyAPIView):
    View to retrieve, update, or delete a single user.
     remove/omit the destroy method to prevent deleting users
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)


def user_details(request, pk):
    """
    View to retrieve a user's profile.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)


class PersonalInfoCreateView(CreateAPIView):
    serializer_class = PersonalInfoSerializer
    queryset = PersonalInfo.objects.all()


# @permission_classes([IsAuthenticated])
class PersonalInfoUpdateView(APIView):
    # retrieve personal info using the user ID and update
    def put(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PersonalInfoSerializer(
            user.personal_info, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Personal info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileInfoCreateView(CreateAPIView):
    serializer_class = ProfileInfoSerializer
    queryset = ProfileInfo.objects.all()


class ProfileInfoUpdateView(APIView):
    # retrieve profile info using the user ID and update
    def put(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # Deserialize the request data and update the user's profile
        serializer = ProfileInfoSerializer(
            user.profile_info, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Profile info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class EducationInfoCreateView(CreateAPIView):
    serializer_class = EducationInfoSerializer
    queryset = EducationInfo.objects.all()


class EducationInfoUpdateView(APIView):
    # retrieve education info using the user ID and update
    def put(self, request, user_id, edu_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # noqa
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            education_info = EducationInfo.objects.get(id=edu_id)
        except EducationInfo.DoesNotExist:
            return JsonResponse(
                {"error": "Education not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EducationInfoSerializer(
            education_info, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Education info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class EducationInfoListView(ListAPIView):
    serializer_class = EducationInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return EducationInfo.objects.filter(user_id=user_id)


class WorkExpInfoCreateView(CreateAPIView):
    serializer_class = WorkExperienceInfoSerializer
    queryset = WorkExperienceInfo.objects.all()


class WorkExpInfoUpdateView(APIView):
    # retrieve personal info using the user ID and update using the expId as
    # the lookup field <userId, expId>
    def put(self, request, user_id, exp_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # noqa

        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            work_experience = WorkExperienceInfo.objects.get(id=exp_id)
        except WorkExperienceInfo.DoesNotExist:
            return JsonResponse(
                {"error": "Work Experience not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = WorkExperienceInfoSerializer(
            work_experience, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Work Experience info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# get a list of work experience info for a user
class WorkExpInfoListView(ListAPIView):
    serializer_class = WorkExperienceInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return WorkExperienceInfo.objects.filter(user_id=user_id)


class AddressInfoCreateView(CreateAPIView):
    serializer_class = AddressInfoSerializer
    queryset = AddressInfo.objects.all()

    # error handling for duplicate address
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError as e:
            return JsonResponse(
                {"error": e},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddressInfoUpdateView(APIView):
    # retrieve profile info using the user ID and update
    def put(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # Deserialize the request data and update the user's profile
        serializer = AddressInfoSerializer(
            user.address_info, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Address info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SocialMediaInfoCreateView(CreateAPIView):
    serializer_class = SocialMediaInfoSerializer
    queryset = SocialMediaInfo.objects.all()


class SocialMediaInfoUpdateView(APIView):
    # retrieve profile info using the user ID and update
    def put(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # Deserialize the request data and update the user's profile
        serializer = SocialMediaInfoSerializer(
            user.social_media_info, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Social Media info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SkillsInfoCreateView(CreateAPIView):
    serializer_class = SkillsInfoSerializer
    queryset = SkillsInfo.objects.all()


# get a list of work experience info for a user
class SkillsInfoListView(ListAPIView):
    serializer_class = SkillsInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return SkillsInfo.objects.filter(user_id=user_id)


class SkillsInfoUpdateView(APIView):
    # retrieve profile info using the user ID and update using the
    # skillId as the lookup field <userId, skillId>
    def put(self, request, user_id, skill_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # noqa
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            skill = SkillsInfo.objects.get(id=skill_id)
        except SkillsInfo.DoesNotExist:
            return JsonResponse(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Deserialize the request data and update the user's profile
        serializer = SkillsInfoSerializer(
            skill, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Skills updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CertificationsInfoCreateView(CreateAPIView):
    serializer_class = CertificationsInfoSerializer
    queryset = CertificationsInfo.objects.all()


class CertificationsInfoUpdateView(APIView):
    def put(self, request, user_id, cert_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # noqa
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            certification = CertificationsInfo.objects.get(id=cert_id)
        except CertificationsInfo.DoesNotExist:
            return JsonResponse(
                {"error": "Certification not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Deserialize the request data and update the user's profile
        serializer = CertificationsInfoSerializer(
            certification, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Certifications updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CertificationsInfoListView(ListAPIView):
    serializer_class = CertificationsInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return CertificationsInfo.objects.filter(user_id=user_id)


class AssociationsInfoCreateView(CreateAPIView):
    serializer_class = AssociationsInfoSerializer
    queryset = AssociationsInfo.objects.all()


class AssociationsInfoUpdateView(APIView):
    # retrieve association info using the user ID and update using the
    # associationId as the lookup field <userId, associationId>
    def put(self, request, user_id, ass_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # noqa
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            association = AssociationsInfo.objects.get(id=ass_id)
        except AssociationsInfo.DoesNotExist:
            return JsonResponse(
                {"error": "Association not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Deserialize the request data and update the user's profile
        serializer = AssociationsInfoSerializer(
            association, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "Association info updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class AssociationsInfoListView(ListAPIView):
    serializer_class = AssociationsInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return AssociationsInfo.objects.filter(user_id=user_id)
