# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r"chapters", views.ChapterViewSet)

# urlpatterns = [
#     path("", include(router.urls)),
#     path(
#         "chapters/search-chapter/<str:chapter_name>/",
#         views.SearchChapter.as_view(),
#         name="by-name",
#     ),
#     path(
#         "chapters/<int:chapter_id>/register/",
#         views.ChapterRegistrationView.as_view(),
#         name="user-register",
#     ),
#     path(
#         "chapter-leaders/<int:chapter_id>/",
#         views.ChapterLeadershipCreateView.as_view(),
#         name="chapter-leaders",
#     ),
#     path(
#         "chapter-leaders/<int:chapter_id>/leaders/<int:user_id>",
#         views.ChapterLeadershipUpdateView.as_view(),
#         name="chapter-leaders-update",
#     ),
#     path(
#         "chapter-leaders/<int:chapter_id>/leaders/",
#         views.ChapterLeadershipListView.as_view(),
#         name="chapter-leaders-list",
#     ),
# ]

from django.urls import path, include
from .views import (
    CachedChapterListView,
    CachedChapterDetailView,
    CachedChapterLeadershipListView,
    CachedSearchChapterView,
    CachedChapterRegistrationView,
)

urlpatterns = [
    # ... other urlpatterns

    # Use the cached views for Chapter
    path('chapters/', CachedChapterListView.as_view({'get': 'list'}), name='chapter-list'),
    path('chapters/<int:pk>/', CachedChapterDetailView.as_view({'get': 'retrieve'}), name='chapter-detail'),

    # Use the cached view for Chapter Leadership
    path('chapters/<int:chapter_id>/leadership/', CachedChapterLeadershipListView.as_view(), name='chapter-leadership-list'),

    # Use the cached view for searching chapters
    path('chapters/search/<str:chapter_name>/', CachedSearchChapterView.as_view(), name='search-chapter'),

    # Use the cached view for Chapter Registration
    path('chapters/<int:chapter_id>/register/', CachedChapterRegistrationView.as_view(), name='chapter-registration'),
]
