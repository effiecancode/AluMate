from typing import Any

import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _

from app.abstracts import (
    IntegerIDModel,
    TimeStampedModel,
)
from app.constant import UserGroup
from app.user_module.constant import scholar_type  # max_value_current_year,


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **kwargs: Any) -> Any:
        """
        Creates and saves a User with the given email address and password
        only if either 'PF' or 'scholar_code' exists in UserData table.
        """
        if not email:
            raise ValueError("Email must be set!")
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **kwargs)
        user.set_password(password)
        group, _ = Group.objects.get_or_create(name=UserGroup.USER)
        user.save(using=self._db)
        user.groups.add(group)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        create_user: Using this method for test cases.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **kwargs: Any
    ) -> Any:
        """creates a superuser with a given email address and password"""
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        try:
            self.model(email=email)
        except ValidationError:
            raise ValueError("Invalid email address")
        superuser = self._create_user(email=email, password=password, **kwargs)
        # assign superuser to super admin group by default
        group, _ = Group.objects.get_or_create(name=UserGroup.SUPER_ADMIN)
        superuser.save(using=self._db)
        superuser.groups.add(group)
        return superuser


class User(
    AbstractBaseUser, PermissionsMixin, TimeStampedModel, IntegerIDModel
):
    """
    Custom user model to replace the default Django User model.
    """

    username = models.CharField(
        verbose_name=_("Display Name"),
        unique=True,
        blank=True,
        max_length=40,
        null=True,
    )
    first_name = models.CharField(verbose_name=_("First Name"), max_length=30)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=30)
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    scholar_type = models.PositiveIntegerField(
        verbose_name=_("Scholar Type"),
        choices=scholar_type,
        blank=True,
        null=True,
    )
    PF = models.CharField(
        verbose_name=_("PF number"),
        max_length=30,
        blank=True,
        null=True,
        unique=True,
    )
    scholar_code = models.CharField(
        verbose_name=_("Scholar Code"),
        max_length=30,
        null=True,
        unique=True,
        blank=True,
    )

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    user_group = models.PositiveIntegerField(
        verbose_name=_("User Group"),
        choices=UserGroup.choices,
        default=UserGroup.USER,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs) -> None:
        if not self.username:
            username = self.email.split("@")[0]
            self.username = username
        if not self.scholar_code:
            self.scholar_code = None
        if not self.PF:
            self.PF = None
        super(User, self).save(*args, **kwargs)

    def get_short_name(self) -> str:
        return self.email

    def get_scholar_code(self) -> None:
        return self.scholar_code

    def assign_user_group(cls, user, user_group):
        try:
            group_name = UserGroup(user_group).label
        except ValueError:
            raise ValidationError(_("Invalid user group."))

        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def get_pf(self) -> None:
        return self.PF

    def get_full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class PersonalInfo(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=55,
        blank=True,
    )
    middle_name = models.CharField(
        verbose_name=_("Second Name"), max_length=30, blank=True
    )
    phone_number = models.CharField(
        verbose_name=_("Primary Phone Number"), max_length=15, blank=True
    )
    additional_phone_number = models.CharField(
        verbose_name=_("Alternate Phone Number"), max_length=15, blank=True
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        blank=True,
        null=True,
        max_length=110,
    )
    dob = models.DateField(
        blank=True, null=True, verbose_name=_("Date of Birth")
    )
    marital_status = models.CharField(
        verbose_name=_("Marital Status"),
        max_length=250,
        blank=True,
    )
    home_branch = models.CharField(
        max_length=100,
        blank=True,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="personal_info"
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " - Personal Info"

    def get_full_name(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.email

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"


class ProfileInfo(models.Model):
    bio = models.CharField(
        verbose_name=_("Bio"), max_length=140, blank=True, null=True
    )
    profile_pic = CloudinaryField("Profile picture", null=True, blank=True)
    scholar_level = models.CharField(
        verbose_name=_("Scholar Education Level"),
        blank=True,
        null=True,
        max_length=30,
    )
    employment_status = models.CharField(
        verbose_name=_("Current Employment Status"),
        max_length=200,
        blank=True,
        null=True,
    )
    cv = CloudinaryField("CV", null=True, blank=True)
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="profile_info",
        blank=True,
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Profile"

    class Meta:
        verbose_name = "Profile Information"
        verbose_name_plural = "Profile Information"


class AssociationsInfo(models.Model):
    name = models.CharField(
        verbose_name=_("Association Name"),
        max_length=100,
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name=_("Role in Association"),
        max_length=100,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="associations_info",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Associations"


class CertificationsInfo(models.Model):
    name = models.CharField(
        verbose_name=_("Certification Name"),
        max_length=100,
        blank=True,
        null=True,
    )
    certificate = CloudinaryField(
        "Certificate",
        blank=True,
        null=True,
    )
    certificate_url = models.URLField(
        verbose_name=_("Certification URL"),
        blank=True,
        null=True,
    )
    date_acquired = models.DateField(
        blank=True, null=True, verbose_name=_("Date Certification Achieved")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certifications_info",
    )

    def __str__(self) -> str:
        return self.name


class SkillsInfo(models.Model):
    name = models.CharField(
        verbose_name=_("Skill"), max_length=100, blank=True, null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills_info",
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Skills"

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class SocialMediaInfo(models.Model):
    twitter = models.URLField(verbose_name=_("Twitter"), blank=True, null=True)
    facebook = models.URLField(
        verbose_name=_("Facebook"), blank=True, null=True
    )
    linkedin = models.URLField(
        verbose_name=_("LinkedIn"), blank=True, null=True
    )
    instagram = models.URLField(
        verbose_name=_("Instagram"), blank=True, null=True
    )
    other_sm_profile = models.URLField(blank=True, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="social_media_info"
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Social Media"

    class Meta:
        verbose_name = "Social Media Information"
        verbose_name_plural = "Social Media Information"


class EducationInfo(models.Model):
    institution_category = models.CharField(
        max_length=130,
        blank=True,
    )
    institution_country = models.CharField(
        max_length=130,
        blank=True,
    )
    institution_name = models.CharField(
        verbose_name=_("School Name"), max_length=100, blank=False
    )
    institution_level = models.CharField(
        verbose_name=_("Institution Level"),
        max_length=230,
        blank=True,
    )
    course_cluster = models.CharField(
        verbose_name=_("Course Cluster"),
        max_length=250,
        blank=True,
    )
    course_name = models.CharField(
        verbose_name=_("Course/Program/Degree Name"), max_length=30, blank=True
    )
    year_of_study = models.PositiveIntegerField(
        verbose_name=_("Year of Study"),
        blank=True,
        null=True,
    )
    start_date = models.DateField(
        blank=True, null=True, verbose_name=_("Start Date")
    )
    graduation_year = models.PositiveIntegerField(
        _("Year of Graduation"),
        validators=[MinValueValidator(1984)],
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="education_info",
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Education"

    class Meta:
        verbose_name = "Education Information"
        verbose_name_plural = "Education Information"


class WorkExperienceInfo(models.Model):
    industry = models.CharField(
        verbose_name=_("Industry"), max_length=30, blank=True
    )
    employer = models.CharField(
        verbose_name=_("Company Name"), max_length=30, blank=True
    )
    # choice - part time, fulltime, contract, internship
    employment_type = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(
        verbose_name=_("Job Title/Position"), max_length=30, blank=True
    )
    description = models.TextField(
        verbose_name=_("Description / Achievements"), blank=True
    )
    start_date = models.DateField(
        blank=True, null=True, verbose_name=_("Start Date")
    )
    end_date = models.DateField(
        blank=True, null=True, verbose_name=_("End Date")
    )
    present_employer = models.BooleanField(
        verbose_name=_("Current Workplace"), default=False
    )
    # if self employed
    type_of_business = models.CharField(
        verbose_name=_("Type of Business"),
        max_length=230,
        blank=True,
    )
    number_of_employees = models.PositiveIntegerField(
        verbose_name=_("Number of Employees"), blank=True, null=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="work_experience_info",
        blank=True,
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Work Experience"

    class Meta:
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experience"


class AddressInfo(models.Model):
    country = models.CharField(
        verbose_name=_("Country Of Residence"),
        max_length=136,
        blank=True,
    )
    residence_county = models.CharField(
        verbose_name=_("County of Residence"),
        max_length=50,
        blank=True,
    )
    home_county = models.CharField(
        verbose_name=_("Home County"),
        max_length=50,
        blank=True,
    )
    po_box = models.CharField(
        verbose_name=_("P.O Box e.g p.o.box 123"), max_length=230
    )
    town = models.CharField(
        verbose_name=_("Nearest/Local Town"), max_length=30
    )
    postal_code = models.CharField(
        verbose_name=_("Postal Code e.g 00100"), max_length=30
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="address_info"
    )

    def __str__(self) -> str:
        return "{}".format(self.user.email.split("@")[0]) + " Address"

    class Meta:
        verbose_name = "Address Information"
        verbose_name_plural = "Address Information"


@receiver(pre_delete, sender=ProfileInfo)
def remove_image_from_cloudinary(
    sender: Any, instance: Any, *args: Any, **kwargs: Any
) -> None:
    if (
        hasattr(instance, "profile_info")
        and instance.profile_info is not None
        and instance.profile_info.profile_pic
        and instance.profile_info.profile_pic.public_id
    ):
        cloudinary.uploader.destroy(
            instance.profile_info.profile_pic.public_id, resource_type="image"
        )


# upload user data
class UserData(models.Model):
    scholar_type = models.CharField(max_length=100, null=True, blank=True)
    scholar_code = models.CharField(max_length=100, null=True, blank=True)
    PF = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return "{} - {}".format(
            self.scholar_type, self.scholar_code or self.PF
        )

    class Meta:
        verbose_name = "Scholar Verification Data"
        verbose_name_plural = "Scholar Verification Data"
