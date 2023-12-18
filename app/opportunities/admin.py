from django.contrib import admin

from app.opportunities.models import (  # ApplicationTracking,
    Department,
    Opportunity,
    OpportunityApplication,
)


class OpportunityAdmin(admin.ModelAdmin):
    model = Opportunity
    list_display = (
        "id",
        "title",
        "department",
        "posted_by",
        "description",
        "total_applications",
    )

    readonly_fields = ("total_applications",)


class OpportunityApplicationAdmin(admin.ModelAdmin):
    model = OpportunityApplication
    list_display = (
        "user",
        "opportunity",
        "get_opportunity_company",
        "get_opportunity_department",
        "status",
    )

    def get_opportunity_company(self, obj):
        return obj.opportunity.company

    get_opportunity_company.short_description = "Company"

    def get_opportunity_department(self, obj):
        return obj.opportunity.department

    get_opportunity_department.short_description = "Department"


class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ("id", "name")


admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(OpportunityApplication, OpportunityApplicationAdmin)
