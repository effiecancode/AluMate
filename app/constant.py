from django.db import models
from django.utils.translation import gettext_lazy as _


class UserGroup(models.IntegerChoices):
    USER = 100, _("User")
    HUB_ADMIN = 200, _("Hub Admin")
    CHAPTER_ADMIN = 300, _("Chapter Admin")
    STAFF_ADMIN = 400, _("Staff Admin")
    SUPER_ADMIN = 500, _("Super Admin")


RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

FEEDBACK_CATEGORY = [
    ("Feature", "Feature"),
    ("Bug", "Bug"),
]