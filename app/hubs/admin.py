from django.contrib import admin

from app.hubs.models import (
    Hub,
    HubRegister,
    HubLeadership
)

class HubLeadershipInline(admin.TabularInline):
    model = HubLeadership
    extra = 0


class HubAdmin(admin.ModelAdmin):
    model = Hub
    inlines = (HubLeadershipInline,)
    list_display = (
        "id",
        "name",
        "description",
        "hub_admin",
    )
    readonly_fields = ("id",)
    list_filter = ("name",)
    search_fields = (
        "name",
        "description",
    )
    filter_horizontal = ("members",)


class HubRegisterAdmin(admin.ModelAdmin):
    model = HubRegister
    list_display = ("id", "hub", "user", "created_at")
    readonly_fields = ("id",)
    list_filter = ("hub",)
    search_fields = (
        "email",
        "hub",
    )


admin.site.register(Hub, HubAdmin)
admin.site.register(HubRegister, HubRegisterAdmin)
admin.site.register(HubLeadership)