import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app.user_module.constant import Application_Status  # SKILLS,
from app.user_module.models import User


class Department(models.Model):
    name = models.CharField(
        max_length=64, verbose_name="Department", unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Departments"


class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    # For external opportunities, company name is required
    company = models.CharField(max_length=255, blank=True, null=True)
    # Internal opportunities will have a department
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="opportunity_department",
        blank=False,
        null=True,
    )
    posted_by = models.ForeignKey(
        User, related_name="opportunity", on_delete=models.CASCADE
    )
    posted_on = models.DateField()
    application_deadline = models.DateField()
    description = models.TextField(blank=True, max_length=255, null=True)
    opportunity_url = models.URLField(
        blank=True, null=True, verbose_name="JD Link"
    )
    # make requirements a list of strings
    opportunity_requirements = models.CharField(
        verbose_name=("Required Skills"),
        # choices=SKILLS,
        max_length=255,
    )
    total_applications = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Opportunities"
        ordering = ("-posted_on",)  # order by date posted. recent jobs first

    def __str__(self) -> str:
        return f"{self.title}"


class OpportunityApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    resume = CloudinaryField("CV", null=True, blank=True)
    cover_letter = CloudinaryField("Cover Letter", null=True, blank=True)
    certificate = CloudinaryField("Certificate", null=True, blank=True)
    applied_on = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=255,
        choices=Application_Status,
        default=Application_Status[0][0],
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.opportunity.total_applications += 1
            self.opportunity.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} applied for {self.opportunity} Opportunity"

    class Meta:
        unique_together = ("user", "opportunity")


@receiver(pre_delete, sender=OpportunityApplication)
def remove_files_from_cloudinary(sender, instance, using, **kwargs) -> None:
    if instance.resume and instance.resume.public_id:
        cloudinary.uploader.destroy(instance.resume.public_id)
    if instance.cover_letter and instance.cover_letter.public_id:
        cloudinary.uploader.destroy(instance.cover_letter.public_id)
    if instance.certificate and instance.certificate.public_id:
        cloudinary.uploader.destroy(instance.certificate.public_id)
