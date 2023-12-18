from django.urls import path
from rest_framework import routers

from app.events.views import (  # event_list,; event_detail,
    EventAttendeeDetailView,
    EventAttendeesCreateViewSet,
    EventAttendeesList,
    EventCreate,
    EventRetrieveUpdateDestroy,
    EventViewSet,
)

router = routers.DefaultRouter()


urlpatterns = [
    path("events/", EventViewSet.as_view({"get": "list"}), name="event-list"),
    path("events/create/", EventCreate.as_view(), name="event-create"),
    path(
        "events/<int:pk>/update/",
        EventRetrieveUpdateDestroy.as_view(),
        name="event-update",
    ),
    path(
        "events/<int:event_id>/registered-attendees/",
        EventAttendeesList.as_view(),
        name="event-attendees-list",
    ),
    path(
        "events/registered-attendees/<int:pk>/",
        EventAttendeeDetailView.as_view(),
        name="event-attendees-detail",
    ),
    path(
        "events/registered-attendees/",
        EventAttendeesCreateViewSet.as_view(),
        name="event-attendees-list-create",
    ),
]
