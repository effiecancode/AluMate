import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_possible_number(phone: str) -> None:
    phone_regex = r"^\+?[\d\s-]+$"
    if not re.match(phone_regex, phone):
        raise ValidationError(_("The phone number entered is not valid."))
