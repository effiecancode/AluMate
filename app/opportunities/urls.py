from django.urls import (
    include,
    path,
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"opportunities", views.OpportunityViewSet, basename="opportunity"
)
router.register(
    r"opportunity-apply",
    views.OpportunityApplicationViewSet,
    basename="opportunity_application",
)
router.register(
    r"departments", views.DepartmentCrudViewSet, basename="department"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "opportunities/opportunity/<str:pk>/",
        views.OpportunityDetail.as_view(),
        name="opportunity-detail",
    ),
]
