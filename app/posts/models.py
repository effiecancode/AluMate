"""
Post and Like models: Creates a post and like object.

Uses the custom User model from user_module.models.
"""

from django.db import models
from ..user_module.models import User


class Post(models.Model):
    """
    Post model: Creates a post object.

    Fields:
        author (ForeignKey): User model.
        title (CharField): Title of the post.
        content (TextField): Content of the post.
        created_at (DateTimeField): Time of creation of the post.
        updated_at (DateTimeField): Time of update of the post.

    Returns:
        Post object with title as the default return field.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
        )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    """
    Like model: Creates a like object.

    Fields:
        user (ForeignKey): User model.
        post (ForeignKey): Post model.
        created_at (DateTimeField): Time of creation of the like.
        is_liked (BooleanField): Tracks if a user had liked a post or not.

    Returns:
        Like object with user and post as the default return field.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} liked {self.post}'
