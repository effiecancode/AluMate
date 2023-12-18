from rest_framework import (
    generics,
    viewsets,
)

from app.events.models import (
    Event,
    EventAttendees,
)
from app.events.serializers import (  # EventAdminSerializer,
    EventAttendeesSerializer,
    EventSerializer,
)


class EventCreate(generics.CreateAPIView):
    serializer_class = EventSerializer


class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventAttendeesCreateViewSet(generics.ListCreateAPIView):
    serializer_class = EventAttendeesSerializer
    queryset = EventAttendees.objects.all()


class EventAttendeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventAttendees.objects.all()
    serializer_class = EventAttendeesSerializer


# view to get all attendees for a specific event
class EventAttendeesList(generics.ListAPIView):
    serializer_class = EventAttendeesSerializer

    def get_queryset(self):
        event_id = int(self.kwargs["event_id"])
        event = Event.objects.get(pk=event_id)

        attendees = EventAttendees.objects.filter(event=event)
        return attendees
