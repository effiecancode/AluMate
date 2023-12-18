from django.db import models

from app.chapters.models import Chapter
from app.events.models import Event
from app.feedback.models import FeedBack
from app.hubs.models import Hub
from app.news.models import Post as Feed
from app.opportunities.models import Opportunity
from app.user_module.models import User


class Analytics(models.Model):
    @staticmethod
    def analyze_data():
        total_users = User.objects.count()
        total_chapters = Chapter.objects.count()
        total_feedback = FeedBack.objects.count()
        total_hubs = Hub.objects.count()
        total_events = Event.objects.count()
        total_opportunities = Opportunity.objects.count()
        total_news = Feed.objects.count()

        # Calculate how many events have been contacted by every hub

        # Calculate other metrics as needed
        # ...

        # Create a dictionary with the analytics data, including the totals
        analyzed_data = {
            "total_users": total_users,
            "total_hubs": total_hubs,
            "total_chapters": total_chapters,
            "total_feedback": total_feedback,
            "total_events": total_events,
            "total_opportunities": total_opportunities,
            "total_news": total_news,
        }

        return analyzed_data

    class Meta:
        verbose_name = "Analytics"
        verbose_name_plural = "Analytics"
