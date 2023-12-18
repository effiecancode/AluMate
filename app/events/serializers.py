from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.events.models import (
    Event,
    EventAttendees,
)

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    #     event_organizer_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "time",
            "venue",
            "charges",
            "description",
            "poster",
            "event_creator",
            # "event_organizer_name",
            "event_organizer_chapter",
            "event_status",
            "event_organizer_hub",
            "event_organizer",
            "hubs_invited",
            "chapters_invited",
            "event_capacity",
            "registered_attendees",
            "registered_attendees_count",
        ]
        read_only_fields = ("id",)

    def get_event_organizer_name(self, obj):
        return obj.get_organizer_name()


class EventAttendeesSerializer(serializers.ModelSerializer):
    """
    Serializes all EventAttendees objects
    """

    event_name = serializers.SerializerMethodField()
    attendee_email = serializers.SerializerMethodField()
    attendee_full_name = serializers.SerializerMethodField()
    attendee_scholar_code = serializers.SerializerMethodField()
    attendee_pf = serializers.SerializerMethodField()

    def get_event_name(self, obj):
        return obj.get_event_name()

    def get_attendee_email(self, obj):
        return obj.get_attendee_email()

    def get_attendee_full_name(self, obj):
        return obj.get_attendee_full_name()

    def get_attendee_scholar_code(self, obj):
        return obj.get_attendee_scholar_code()

    def get_attendee_pf(self, obj):
        return obj.get_attendee_pf()

    class Meta:
        model = EventAttendees
        fields = (
            "id",
            "event",
            "attendee",
            "event_name",
            "attendee_email",
            "attendee_full_name",
            "attendee_scholar_code",
            "attendee_pf",
        )
        read_only_fields = ("id",)
