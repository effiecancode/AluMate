from django.urls import (
    include,
    path,
)
from rest_framework import routers

from .views import (
    CommentViewSet,
    LikeViewSet,
    PostViewSet,
)

router = routers.DefaultRouter()
router.register(r"news", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"likes", LikeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
