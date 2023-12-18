from django.contrib import admin

from app.events.models import (
    Event,
    EventAttendees,
    Tag,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = (
        "name",
        "date",
        "time",
        "venue",
        "charges",
        "event_capacity",
        "registered_attendees_count",
    )
    list_filter = (
        "date",
        "event_creator",
        "name",
    )
    search_fields = ("name", "venue", "event_creator")
    ordering = ("-date", "-time")

    readonly_fields = ("registered_attendees_count",)
    filter_horizontal = (
        "hubs_invited",
        "chapters_invited",
        "registered_attendees",
        "tags",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("hubs_invited", "chapters_invited")
        )

    def event_organizer_name(self, obj):
        return obj.get_organizer_name()

    event_organizer_name.admin_order_field = "event_organizer"
    event_organizer_name.short_description = "Event Organizer Name"


class EventAttendeesAdmin(admin.ModelAdmin):
    model = EventAttendees
    list_display = (
        "get_event",
        "get_attendee_full_name",
        "get_attendee_email",
        "get_attendee_pf",
        "get_attendee_scholar_code",
    )
    list_filter = ("event", "attendee")
    search_fields = (
        "get_event",
        "get_attendee_full_name",
        "get_attendee_email",
    )
    ordering = ("event", "attendee")

    def get_event(self, obj):
        return obj.event.name

    def get_attendee_email(self, obj):
        return obj.attendee.email if obj.attendee else None

    def get_attendee_full_name(self, obj):
        return (
            obj.attendee.first_name + " " + obj.attendee.last_name
            if obj.attendee
            else None
        )

    def get_attendee_scholar_code(self, obj):
        return obj.attendee.scholar_code if obj.attendee else None

    def get_attendee_pf(self, obj):
        return obj.attendee.PF if obj.attendee else None

    get_event.short_description = "Event"
    get_attendee_email.short_description = "Email"
    get_attendee_full_name.short_description = "Full Name"
    get_attendee_scholar_code.short_description = "Scholar Code"
    get_attendee_pf.short_description = "PF Number"


admin.site.register(EventAttendees, EventAttendeesAdmin)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Tag, TagAdmin)
