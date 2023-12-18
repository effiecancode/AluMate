from typing import Any
from django.db import models
import cloudinary.uploader
from cloudinary.models import CloudinaryField

from app.constant import FEEDBACK_CATEGORY

"""
FeedBack Class.

Creates a user feedback model. The user can be anonymous and \
    hence not registred in our database. There is, therefore,\
        no need to import the user model.
"""


class FeedBack(models.Model):
    email = models.EmailField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=None, blank=True, null=True)
    feedback = models.TextField(null=True, blank=True)
    # detailed feedback
    feedback_category = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    attachment = CloudinaryField("feedback", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"Feedback {self.id} by {self.email}"


def remove_image_from_cloudinary(
    sender: Any, instance: FeedBack, *args: Any, **kwargs: Any
) -> None:
    if (
        hasattr(instance, "image")
        and instance.attachment is not None
        and instance.attachment.public_id
    ):
        cloudinary.uploader.destroy(
            instance.attachment.public_id, resource_type="image"
        )
