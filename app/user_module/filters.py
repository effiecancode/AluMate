from typing import Any

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from app.user_module.models import (
    EducationInfo,
    PersonalInfo,
    ProfileInfo,
    WorkExperienceInfo,
)

User = get_user_model()


class UserInsightFilter(filters.FilterSet):  # type: ignore[no-any-unimported]
    first_name = filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )
    scholar_type = filters.NumberFilter(
        field_name="scholar_type", lookup_expr="exact"
    )
    PF = filters.NumberFilter(field_name="PF", lookup_expr="exact")
    PF__gt = filters.NumberFilter(field_name="PF", lookup_expr="gte")
    PF__lt = filters.NumberFilter(field_name="PF", lookup_expr="lte")
    scholar_code = filters.CharFilter(
        field_name="scholar_code", lookup_expr="exact"
    )
    scholar_code__gt = filters.CharFilter(
        field_name="scholar_code", lookup_expr="gte"
    )
    scholar_code__lt = filters.NumberFilter(
        field_name="scholar_code", lookup_expr="lte"
    )
    scholar_level = filters.ModelChoiceFilter(
        field_name="scholar_level",
        queryset=ProfileInfo.objects.all(),
        to_field_name="id",
        # lookup_expr="icontains"
    )
    home_branch = filters.ModelChoiceFilter(
        field_name="home_branch",
        queryset=PersonalInfo.objects.all(),
        to_field_name="id",
    )
    institution_name = filters.ModelChoiceFilter(
        field_name="institution_name",
        queryset=EducationInfo.objects.all(),
        to_field_name="id",
    )
    graduation_year = filters.ModelChoiceFilter(
        field_name="graduation_year",
        queryset=EducationInfo.objects.all(),
        to_field_name="id",
    )
    industry = filters.ModelChoiceFilter(
        field_name="industry",
        queryset=WorkExperienceInfo.objects.all(),
        to_field_name="id",
    )
    employment_status = filters.ModelChoiceFilter(
        field_name="employment_status",
        queryset=ProfileInfo.objects.all(),
        to_field_name="id",
    )
    course_name = filters.ModelChoiceFilter(
        field_name="course_name",
        queryset=EducationInfo.objects.all(),
        to_field_name="id",
    )
    year_of_study = filters.ModelChoiceFilter(
        field_name="year_of_study",
        queryset=EducationInfo.objects.all(),
        to_field_name="id",
    )

    def filter_by_institution_name(
        self, queryset: Any, name: str, value: str
    ) -> Any:
        if value.lower() == "true":
            return queryset.exclude(institution_name__isnull=True).exclude(
                created_by__exact=""
            )

        return queryset

    order_by = filters.OrderingFilter(
        fields=(
            ("first_name", "first_name"),
            ("hub", "hub"),
            ("chapter", "chapter"),
            ("scholar_type", "scholar_type"),
        )
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "scholar_type",
            "PF",
            "scholar_code",
            "scholar_level",
            "home_branch",
            "institution_name",
            "graduation_year",
            "industry",
            "employment_status",
            "course_name",
        ]
