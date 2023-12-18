from django.urls import path

from .views import (
    AddressInfoCreateView,
    AddressInfoUpdateView,
    AssociationsInfoCreateView,
    AssociationsInfoListView,
    AssociationsInfoUpdateView,
    CertificationsInfoCreateView,
    CertificationsInfoListView,
    CertificationsInfoUpdateView,
    CustomUserCreateView,
    CustomUserListView,
    CustomUserRetrieveUpdateDestroyView,
    EducationInfoCreateView,
    EducationInfoListView,
    EducationInfoUpdateView,
    FindUserView,
    PersonalInfoCreateView,
    PersonalInfoUpdateView,
    ProfileInfoCreateView,
    ProfileInfoUpdateView,
    SkillsInfoCreateView,
    SkillsInfoListView,
    SkillsInfoUpdateView,
    SocialMediaInfoCreateView,
    SocialMediaInfoUpdateView,
    WorkExpInfoCreateView,
    WorkExpInfoListView,
    WorkExpInfoUpdateView,
    user_details,
)

urlpatterns = [
    path("user/", FindUserView.as_view()),
    path(
        "user/userList/",
        CustomUserListView.as_view(),
        name="user-list",
    ),
    path(
        "user/get-user/<str:pk>/",
        CustomUserRetrieveUpdateDestroyView.as_view(),
        name="user-detail",
    ),
    path(
        "user/register/",
        CustomUserCreateView.as_view(),
        name="user-create",
    ),
    path("user/details/<str:pk>/", user_details, name="user-detail"),
    # personal info
    path("personal-info/", PersonalInfoCreateView.as_view()),
    path(
        "personal-info/update/<int:user_id>/",
        PersonalInfoUpdateView.as_view(),
        name="update-personal-info",
    ),
    # profile info
    path("profile-info/", ProfileInfoCreateView.as_view()),
    path(
        "profile-info/update/<int:user_id>/",
        ProfileInfoUpdateView.as_view(),
        name="update-profile-info",
    ),
    # work experience info
    path("work-experience-info/", WorkExpInfoCreateView.as_view()),
    path(
        "work-experience-info/update/<int:user_id>/exp/<int:exp_id>/",
        WorkExpInfoUpdateView.as_view(),
        name="update-work-experience-info",
    ),
    # work experience list for a user
    path(
        "work-experience-info/<int:user_id>/",
        WorkExpInfoListView.as_view(),
    ),
    # education info
    path("education-info/", EducationInfoCreateView.as_view()),
    path(
        "education-info/update/<int:user_id>/education/<int:edu_id>/",
        EducationInfoUpdateView.as_view(),
    ),
    path(
        "education-info/<int:user_id>/",
        EducationInfoListView.as_view(),
    ),
    # skills info
    path("skills-info/", SkillsInfoCreateView.as_view()),
    path(
        "skills-info/<int:user_id>/",
        SkillsInfoListView.as_view(),
    ),
    path(
        "skills-info/update/<int:user_id>/skill/<int:skill_id>/",
        SkillsInfoUpdateView.as_view(),
    ),
    # social media info
    path("social-media-info/", SocialMediaInfoCreateView.as_view()),
    path(
        "social-media-info/update/<int:user_id>/",
        SocialMediaInfoUpdateView.as_view(),
    ),
    # address info
    path("address-info/", AddressInfoCreateView.as_view()),
    path(
        "address-info/update/<int:user_id>/", AddressInfoUpdateView.as_view()
    ),
    #     associations info
    path("associations-info/", AssociationsInfoCreateView.as_view()),
    path(
        "associations-info/update/<int:user_id>/association/<int:ass_id>/",
        AssociationsInfoUpdateView.as_view(),
    ),
    path(
        "associations-info/<int:user_id>/",
        AssociationsInfoListView.as_view(),
    ),
    #     certifications info
    path("certifications-info/", CertificationsInfoCreateView.as_view()),
    path(
        "certifications-info/update/<int:user_id>/certification/<int:cert_id>/",
        CertificationsInfoUpdateView.as_view(),
    ),
    path(
        "certifications-info/<int:user_id>/",
        CertificationsInfoListView.as_view(),
    ),
]
