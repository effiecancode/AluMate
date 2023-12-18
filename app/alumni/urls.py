from django.urls import path

from .views import AlumniInsights

urlpatterns = [
    path(
        "alumni/",
        AlumniInsights.as_view(),
        name="alumni-insights",
    )
]
