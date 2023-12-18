from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    HubRegisterListCreateView,
    HubRegisterRetrieveUpdateDestroyView,
    HubViewSet,
    HubLeadershipCreateView,
    HubLeadershipListView,
    HubLeadershipUpdateView
)

router = DefaultRouter()
router.register(r"hubs", HubViewSet, basename="hubs")

urlpatterns = [
    path(
        "hubs/user_register/",
        HubRegisterListCreateView.as_view(),
        name="hub-user-register",
    ),
    path(
        "hubs/register/<int:pk>/",
        HubRegisterRetrieveUpdateDestroyView.as_view(),
        name="hub-register-retrieve-update-destroy",
    ),
        path(
        "hub-leaders/<int:hub_id>/",
        HubLeadershipCreateView.as_view(),
        name="hub-leaders",
    ),
    path(
        "hub-leaders/<int:hub_id>/leaders/<int:user_id>",
        HubLeadershipUpdateView.as_view(),
        name="hub-leaders-update",
    ),
    path(
        "hub-leaders/<int:hub_id>/leaders/",
        HubLeadershipListView.as_view(),
        name="hub-leaders-list",
    ),
]

urlpatterns += router.urls
