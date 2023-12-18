from typing import Any

import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app.user_module.models import User

from .constants import STATUS_CHOICES


class Post(models.Model):
    content = models.TextField()
    poster = CloudinaryField("Post Poster", blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )
    # approver nust be an admin
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="approved_posts",
        blank=True,
        null=True,
    )
    created_at = models.DateField(auto_now_add=True)
    visible = models.BooleanField(default=True, null=True, blank=True)
    # likes = models.ManyToManyField(
    #     User, related_name="liked_posts", blank=True
    # )
    # comments = models.ManyToManyField(
    #     User, related_name="commented_posts", blank=True
    # )
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} by {self.posted_by.username}"

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save(update_fields=["likes_count"])

    def update_comments_count(self):
        self.comments_count = self.comments.count()
        self.save(update_fields=["comments_count"])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_comments"
    )
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id} by {self.author.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_comment_count()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_comment_count()

    def update_comment_count(self):
        self.post.comments_count = self.post.post_comments.count()
        self.post.save(update_fields=["comments_count"])


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes"
    )
    liked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes"
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "liked_by")

    def __str__(self):
        return f"Like {self.id} on Post {self.post.id} by {self.liked_by.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_like_count()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_like_count()

    def update_like_count(self):
        self.post.likes_count = self.post.likes.count()
        self.post.save(update_fields=["likes_count"])


@receiver(pre_delete, sender=Post)
def remove_image_from_cloudinary(
    sender: Any, instance: Any, *args: Any, **kwargs: Any
) -> None:
    if instance.poster and instance.poster.public_id:
        cloudinary.uploader.destroy(
            instance.poster.public_id, resource_type="image"
        )
