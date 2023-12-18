from django.urls import path

from .views import AnalyticsAPIView

urlpatterns = [
    path("analytics/", AnalyticsAPIView.as_view(), name="analytics"),
]
