from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer

class PostLikeApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')

    def test_create_like(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )
        data = {'post': post.id}
        response = self.client.post('/api/like/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().user, self.user)

    def test_unlike_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )
        like = Like.objects.create(user=self.user, post=post, is_liked=True)
        response = self.client.put(f'/api/unlike/{like.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        like.refresh_from_db()
        self.assertFalse(like.is_liked)

    def test_unlike_post_permission_denied(self):
        # Create a post and like associated with a different user
        other_user = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='otherpassword'
        )
        post = Post.objects.create(
            author=other_user,
            title='Test Post',
            content='Test Content'
        )
        like = Like.objects.create(user=other_user, post=post, is_liked=True)
        response = self.client.put(f'/api/unlike/{like.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        like.refresh_from_db()
        self.assertTrue(like.is_liked)

    def test_like_not_found(self):
        # Attempt to unlike a non-existent like
        response = self.client.put('/api/unlike/999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
