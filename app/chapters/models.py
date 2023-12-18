from typing import Any

import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app.abstracts import TimeStampedModel, IntegerIDModel

User = get_user_model()




class Chapter(IntegerIDModel):
    name = models.CharField(max_length=100, unique=True, blank=False)
    chapter_profile_image = CloudinaryField("chapter", null=True, blank=True)
    institution = models.CharField(max_length=100, blank=False)
    registration_fee = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=250)
    members = models.ManyToManyField(
        User,
        related_name="chapters",
        blank=True,
        verbose_name="Chapter Members"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    chapter_admin = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Chapters"

    def __str__(self) -> str:
        return self.name
    
    
class ChapterLeadership(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="chapter_leaders")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Leaders"
    )
    role = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.chapter.name}"

    class Meta:
        verbose_name_plural = "Chapter Leadership"
        unique_together = ("chapter", "user")



@receiver(pre_delete, sender=Chapter)
def remove_image_from_cloudinary(
    sender: Any, instance: Chapter, *args: Any, **kwargs: Any
) -> None:
    if (
        instance.chapter_profile_image
        and instance.chapter_profile_image.public_id
    ):
        cloudinary.uploader.destroy(
            instance.chapter_profile_image.public_id,
            invalidate=True,
            resource_type="image",
        )


class ChapterRegister(TimeStampedModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Members"
    )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.chapter.name}"

    class Meta:
        verbose_name_plural = "Chapter Registers"
        unique_together = ("chapter", "user")
