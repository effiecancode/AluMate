from typing import Any

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from app.user_module.models import (
    AddressInfo,
    EducationInfo,
    PersonalInfo,
    ProfileInfo,
    WorkExperienceInfo,
)

User = get_user_model()


def filter_by_institution_name(queryset: Any, name: str, value: str) -> Any:
    if value.lower() == "true":
        return queryset.exclude(institution_name__isnull=True).exclude(
            created_by__exact=""
        )

    return queryset


class UserProfileInsightFilter(filters.FilterSet):  # type: ignore[no-any-unimported]
    first_name = filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )
    scholar_type = filters.NumberFilter(
        field_name="scholar_type", lookup_expr="icontains"
    )
    PF = filters.NumberFilter(field_name="PF", lookup_expr="icontains")
    PF__gt = filters.NumberFilter(field_name="PF", lookup_expr="gte")
    PF__lt = filters.NumberFilter(field_name="PF", lookup_expr="lte")
    scholar_code = filters.CharFilter(
        field_name="scholar_code", lookup_expr="icontains"
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
    hub = filters.ModelChoiceFilter(
        field_name="hub",
        queryset=AddressInfo.objects.all(),
        to_field_name="id",
    )
    chapter = filters.ModelChoiceFilter(
        field_name="chapter",
        queryset=AddressInfo.objects.all(),
        to_field_name="id",
    )

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
            "hub",
            "chapter",
        ]
