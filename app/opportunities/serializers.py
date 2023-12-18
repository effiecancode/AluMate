from rest_framework import serializers

from app.utils import CommaSeparatedWordsField

from .models import (  # ApplicationTracking,
    Department,
    Opportunity,
    OpportunityApplication,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class OpportunitySerializer(serializers.ModelSerializer):
    opportunity_requirements = CommaSeparatedWordsField(
        child=serializers.CharField(),
    )

    class Meta:
        model = Opportunity
        fields = (
            "id",
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


class OpportunityApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunityApplication
        fields = "__all__"
