from django.urls import (
    include,
    path,
)
from rest_framework import routers

from .views import FeedBackViewSet

router = routers.DefaultRouter()
router.register(r"feedback", FeedBackViewSet, basename="feedback")

urlpatterns = [
    path("", include(router.urls)),
]
