from django.contrib import admin

from app.user_module.models import (  # imported; OtherInfo,
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


class SkillsInfoAdmin(admin.ModelAdmin):
    model = SkillsInfo
    list_display = (
        "user",
        # "employment_status",
        # "years_of_experience",
        "name",
    )


admin.site.register(SkillsInfo, SkillsInfoAdmin)


class SocialMediaInfoAdmin(admin.ModelAdmin):
    model = SocialMediaInfo
    list_display = (
        "user",
        "facebook",
        "twitter",
        "linkedin",
        "instagram",
    )


admin.site.register(SocialMediaInfo, SocialMediaInfoAdmin)


class EducationInfoAdmin(admin.ModelAdmin):
    model = EducationInfo
    list_display = (
        "user",
        "institution_category",
        "institution_name",
        "course_name",
        "graduation_year",
    )


admin.site.register(EducationInfo, EducationInfoAdmin)


class AddressInfoAdmin(admin.ModelAdmin):
    model = AddressInfo
    list_display = (
        "user",
        "country",
        "home_county",
        "residence_county",
        "town",
    )


admin.site.register(AddressInfo, AddressInfoAdmin)


class PersonalInfoAdmin(admin.ModelAdmin):
    model = PersonalInfo
    list_display = (
        "user",
        "title",
        "middle_name",
        "home_branch",
        "phone_number",
    )


admin.site.register(PersonalInfo, PersonalInfoAdmin)


class ProfileInfoAdmin(admin.ModelAdmin):
    model = ProfileInfo
    list_display = (
        "user",
        "profile_pic",
        "bio",
    )


admin.site.register(ProfileInfo, ProfileInfoAdmin)


class UserDataAdmin(admin.ModelAdmin):
    model = UserData
    list_display = (
        "scholar_type",
        "PF",
        "scholar_code",
    )


admin.site.register(UserData, UserDataAdmin)


class WorkExperienceInfoAdmin(admin.ModelAdmin):
    model = WorkExperienceInfo
    list_display = (
        "user",
        "industry",
        "employer",
        "job_title",
        "start_date",
    )


admin.site.register(WorkExperienceInfo, WorkExperienceInfoAdmin)


class AssociationsInfoAdmin(admin.ModelAdmin):
    model = AssociationsInfo
    list_display = (
        "user",
        "name",
        "role",
    )


admin.site.register(AssociationsInfo, AssociationsInfoAdmin)


class CertificationsInfoAdmin(admin.ModelAdmin):
    model = CertificationsInfo
    list_display = (
        "user",
        "name",
        "certificate",
        "date_acquired",
    )


admin.site.register(CertificationsInfo, CertificationsInfoAdmin)
