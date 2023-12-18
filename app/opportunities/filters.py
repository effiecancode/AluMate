# search opportunity by title, company, department, posted_by, posted_on,
# description, application_deadline, opportunity_url, opportunity_requirements

# Path: app/opportunities/urls.py
from django_filters import rest_framework as filters

from app.opportunities.views import (  # ApplicationTracking,; OpportunityApplication,
    Department,
    Opportunity,
)


class OpportunityFilters(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    company = filters.CharFilter(lookup_expr="icontains")
    department = filters.CharFilter(lookup_expr="icontains")
    posted_by = filters.CharFilter(lookup_expr="icontains")
    posted_on = filters.DateFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    application_deadline = filters.DateFilter(lookup_expr="icontains")
    opportunity_url = filters.CharFilter(lookup_expr="icontains")
    opportunity_requirements = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Opportunity
        fields = (
            "title",
            "company",
            "department",
            "posted_by",
            "posted_on",
            "description",
            "application_deadline",
            "opportunity_url",
            "opportunity_requirements",
        )


class DepartmentFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Department
        fields = ("name",)
