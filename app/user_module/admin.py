from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import (  # imported; OtherInfo,
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

User = get_user_model()


class SkillsInfoInline(admin.TabularInline):
    model = SkillsInfo
    extra = 0


class PersonalInfoInline(admin.TabularInline):
    model = PersonalInfo
    extra = 0


class SocialMediaInfoInline(admin.TabularInline):
    model = SocialMediaInfo
    extra = 0


class AddressInfoInline(admin.TabularInline):
    model = AddressInfo
    extra = 0


class ProfileInfoInline(admin.TabularInline):
    model = ProfileInfo
    extra = 0


class EducationInfoInline(admin.TabularInline):
    model = EducationInfo
    extra = 0


class WorkExperienceInfoInline(admin.TabularInline):
    model = WorkExperienceInfo
    extra = 0


class CertificationsInfoInline(admin.TabularInline):
    model = CertificationsInfo
    extra = 0


class AssociationsInfoInline(admin.TabularInline):
    model = AssociationsInfo
    extra = 0


class UserAdmin(DjangoUserAdmin):
    model = User
    inlines = [
        ProfileInfoInline,
        PersonalInfoInline,
        SkillsInfoInline,
        EducationInfoInline,
        CertificationsInfoInline,
        AssociationsInfoInline,
        WorkExperienceInfoInline,
        # OtherInfoInline,
        SocialMediaInfoInline,
        AddressInfoInline,
    ]
    list_display = (
        # "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "user_group",
        "user_phone_number",
    )

    list_filter = ("is_staff", "is_superuser")
    search_fields = ("email", "first_name", "username", "last_name")
    ordering = ("first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password",
                    "scholar_type",
                    "scholar_code",
                    "PF",
                )
            },
        ),
        (
            "Contact info",
            {"fields": ("email",)},
        ),
        ("Important dates", {"fields": ("last_login",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_group",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "scholar_type",
                    "scholar_code",
                    "PF",
                ),
            },
        ),
        # (
        #     "Contact info",
        #     {"fields": ("phone_number",)},
        # ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_group",
                )
            },
        ),
    )

    def user_phone_number(self, obj: PersonalInfo) -> str:
        try:
            return obj.phone_number

        except Exception:
            return ""


admin.site.register(User, UserAdmin)
