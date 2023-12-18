from typing import Any
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.events.utils import generate_number


class TimeStampedModel(models.Model):
    """
    This is an abstract base class that allows us to put common fields created_at and updated at that can be used in a number of models.
    """

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"), auto_now=True, null=True
    )

    class Meta:
        """
        We put abstract=True in the Meta class so that the model will not be used to create any database table.
        Instead, when it is used as a base class for other models, its fields will be added to those of the child class.
        """

        abstract = True
        ordering = (
            "created_at",
            "updated_at",
        )


class IDModel(models.Model):
    """
    An abstract base class that allows us to generate a unique id for each model.
    """

    id = models.CharField(primary_key=True, max_length=255, editable=False)

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> Any:
        if not self.id:
            is_unique = False
            while not is_unique:
                id = uuid4().hex
                is_unique = not self.__class__.objects.filter(id=id).exists()

            self.id = id
        return super().save(*args, **kwargs)


class IntegerIDModel(models.Model):
    """
    An abstract base class that allows us to generate a unique integer id for each model.
    """

    id = models.CharField(primary_key=True, max_length=255, editable=False)

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> Any:
        if not self.id:
            is_unique = False
            while not is_unique:
                id = generate_number(num_digits=12)
                is_unique = not self.__class__.objects.filter(id=id).exists()

            self.id = id
        return super().save(*args, **kwargs)
