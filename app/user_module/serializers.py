from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.constant import UserGroup
from app.user_module.models import (
    AddressInfo,
    AssociationsInfo,
    CertificationsInfo,
    EducationInfo,
    PersonalInfo,
    ProfileInfo,
    SkillsInfo,
    SocialMediaInfo,
    UserData,
    WorkExperienceInfo,
)

User = get_user_model()


class PersonalInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the PersonalInfo model.
    """

    class Meta:
        model = PersonalInfo
        fields = "__all__"


class WorkExperienceInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkExperienceInfo model.
    """

    class Meta:
        model = WorkExperienceInfo
        fields = "__all__"


class EducationInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Education model.
    """

    class Meta:
        model = EducationInfo
        fields = "__all__"


class CertificationsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationsInfo
        # exclude = ["user", "id"]
        fields = (
            "id",
            "user",
            "name",
            "certificate",
            "certificate_url",
            "date_acquired",
        )


class AssociationsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociationsInfo
        fields = "__all__"


class ProfileInfoSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = ProfileInfo
        fields = "__all__"


class AddressInfoSerializer(serializers.ModelSerializer):
    po_box = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    home_county = serializers.CharField(required=False)
    residence_county = serializers.CharField(required=False)
    town = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)

    class Meta:
        model = AddressInfo
        fields = "__all__"


class SkillsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsInfo
        fields = (
            "id",
            "user",
            "name",
        )


#


class SocialMediaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaInfo
        fields = "__all__"


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ("scholar_type", "scholar_code", "PF")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    username = serializers.CharField(required=False)
    scholar_type = serializers.CharField()
    user_group = serializers.ChoiceField(choices=UserGroup, default="100")
    scholar_code = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
        allow_null=True,
    )
    PF = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    personal_info = PersonalInfoSerializer(required=False)
    address_info = AddressInfoSerializer(required=False)
    work_experience_info = WorkExperienceInfoSerializer(
        many=True, required=False
    )
    education_info = EducationInfoSerializer(many=True, required=False)
    profile_info = ProfileInfoSerializer(required=False)
    skills_info = SkillsInfoSerializer(many=True, required=False)
    social_media_info = SocialMediaInfoSerializer(required=False)
    associations_info = AssociationsInfoSerializer(many=True, required=False)
    certifications_info = CertificationsInfoSerializer(
        many=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "scholar_type",
            "PF",
            "scholar_code",
            "password",
            "date_joined",
            "is_active",
            # "scholar_level",
            "is_staff",
            "user_group",
            "personal_info",
            "profile_info",
            "education_info",
            "skills_info",
            "work_experience_info",
            "associations_info",
            "certifications_info",
            "social_media_info",
            "address_info",
        )
        depth = 1
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = (
            "id",
            "user_group",
        )

    def validate_scholar_code(self, scholar_code: str):
        if not UserData.objects.filter(Q(scholar_code=scholar_code)).exists():
            raise serializers.ValidationError("Scholar code does not exist.")
        return scholar_code

    def validate_PF(self, PF: str):
        if not UserData.objects.filter(Q(PF=PF)).exists():
            raise serializers.ValidationError("PF does not exist.")
        return PF

    def validate_username(self, username: str):
        if User.objects.filter(Q(username=username)).exists():
            raise serializers.ValidationError("Username already exists.")
        return username

    def validate_password(self, value: str):
        """
        User password validation.

        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if value.isalpha():
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        if value.isnumeric():
            raise serializers.ValidationError(
                "Password must contain at least one letter."
            )
        if value.islower():
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if value.isupper():
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if value.isalnum():
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
        return make_password(value)
