from django.urls import path
from . import views


urlpatterns = [
    # Endpoint for creating and listing posts
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),

    # Endpoint for creating likes
    path('like/', views.LikeCreateView.as_view(), name='like-create'),

    # Endpoint for toggling likes (unliking)
    path('unlike/<int:pk>/', views.UnlikeView.as_view(), name='unlike'),
]
