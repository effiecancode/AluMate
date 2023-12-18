from typing import Any

import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.abstracts import (
    IntegerIDModel,
    TimeStampedModel,
)
from app.chapters.models import Chapter
from app.hubs.models import Hub
from app.user_module.constant import (
    Event_Status,
    Organizer_Choices,
)
from app.user_module.models import User


class Tag(IntegerIDModel, TimeStampedModel):
    """
    This model deals with all the tags that will be used to categorize events.

    attrs:
        name: name of the tag
    """

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events:tag-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("events:tag-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("events:tag-delete", kwargs={"pk": self.pk})


class Event(IntegerIDModel, TimeStampedModel):
    """
    This model deals with all the events that will be organised.
    There will only be one event_organizer but many invitees can attend.

    attrs:
        name: name of the event
        venue: place the event should be held
        event_organizer: event's planner (hub, chapter, or user)
        date: date the event should be happening
        time: time the event should be happening
        description: what the event is all about
        invitees: who should attend the event
    """

    class Meta:
        ordering = ["-date", "-time"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    poster = CloudinaryField("Event Poster", null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    charges = models.FloatField(
        verbose_name=_("charges"), null=True, blank=True
    )
    description = models.TextField()
    event_organizer = models.CharField(
        max_length=10,
        choices=Organizer_Choices,
        default=Organizer_Choices[0][1],
    )
    event_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    event_organizer_chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, blank=True, null=True
    )
    event_organizer_hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, blank=True, null=True
    )
    event_status = models.CharField(
        max_length=30,
        choices=Event_Status,
        default=Event_Status[1][0],
    )
    event_capacity = models.PositiveIntegerField(default=None, null=True)
    hubs_invited = models.ManyToManyField(
        Hub, blank=True, related_name="events_invited_to"
    )
    chapters_invited = models.ManyToManyField(
        Chapter, related_name="events_invited_to", blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    registered_attendees = models.ManyToManyField(
        User, related_name="Users_attending_Event", blank=True
    )
    # auto-calculate the number of registered attendees
    registered_attendees_count = models.PositiveIntegerField(
        default=0, verbose_name=_("To Attend")
    )

    def __str__(self):
        return self.name

    @property
    def event_organizer_object(self):
        if self.event_organizer == "hub":
            return self.event_organizer_hub
        elif self.event_organizer == "chapter":
            return self.event_organizer_chapter
        elif self.event_organizer == "user":
            return self.event_creator
        else:
            return None

    def get_organizer_name(self):
        if self.event_organizer == "hub":
            return (
                self.event_organizer_hub.name
                if self.event_organizer_hub
                else None
            )
        elif self.event_organizer == "chapter":
            return (
                self.event_organizer_chapter.name
                if self.event_organizer_chapter
                else None
            )
        elif self.event_organizer == "user":
            return (
                self.event_creator.get_full_name()
                or self.event_creator.username
                if self.event_creator
                else None
            )
        else:
            return None

    def get_absolute_url(self):
        return reverse("events:event_detail", args=[str(self.id)])


@receiver(pre_delete, sender=Event)
def remove_image_from_cloudinary(
    sender: Any, instance: Any, *args: Any, **kwargs: Any
) -> None:
    if (
        hasattr(instance, "poster")
        and instance.poster is not None
        and instance.poster.public_id
    ):
        cloudinary.uploader.destroy(
            instance.poster.public_id, resource_type="image"
        )


class EventAttendees(IntegerIDModel, TimeStampedModel):
    """
    This model deals with all the attendees of an event.
    """

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("event", "attendee")
        verbose_name = "Event Attendee"
        verbose_name_plural = "Event Attendees"

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_event_name(self):
        return self.event.name if self.event else None

    def get_attendee_full_name(self):
        return (
            self.attendee.get_full_name() or self.attendee.username
            if self.attendee
            else None
        )

    def get_attendee_email(self):
        return self.attendee.email if self.attendee else None

    def get_attendee_scholar_code(self):
        return self.attendee.scholar_code if self.attendee else None

    def get_attendee_pf(self):
        return self.attendee.PF if self.attendee else None

    def __str__(self):
        return f"{self.attendee} attending {self.event}"

    """ensure that a user can only register for an event once
    append the attendee to the list of registered attendees
    add the attendee to the list of registered attendees, if not already registered"""

    def save(self, *args, **kwargs):
        if not self.id:
            # New instance, increase total registered attendees count
            self.event.registered_attendees_count += 1
            self.event.save()

        super().save(*args, **kwargs)

        # Update the registered_attendees field in the Event model
        self.event.registered_attendees.add(self.attendee)
