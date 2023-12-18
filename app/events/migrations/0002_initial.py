# Generated by Django 4.2.3 on 2023-08-10 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("chapters", "0002_initial"),
        ("hubs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventattendees",
            name="attendee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="eventattendees",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="events.event"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="chapters_invited",
            field=models.ManyToManyField(
                blank=True,
                related_name="events_invited_to",
                to="chapters.chapter",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="event_creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="event_organizer_chapter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chapters.chapter",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="event_organizer_hub",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hubs.hub",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="hubs_invited",
            field=models.ManyToManyField(
                blank=True, related_name="events_invited_to", to="hubs.hub"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="registered_attendees",
            field=models.ManyToManyField(
                blank=True,
                related_name="Users_attending_Event",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="tags",
            field=models.ManyToManyField(blank=True, to="events.tag"),
        ),
    ]