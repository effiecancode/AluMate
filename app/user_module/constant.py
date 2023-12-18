import datetime

from django.core.validators import MaxValueValidator  # noqa


def current_year() -> int:
    return datetime.date.today().year


def max_value_current_year(value) -> None:
    return MaxValueValidator(current_year())(value)


scholar_type = [
    (1, "ELP"),
    (2, "WTF"),
    (3, "Both"),
]

# Backend
Opportunity_Status = [
    ("Not Applied", "Not Applied"),
    ("Applied", "Applied"),
]

# Backend
Application_Status = [
    ("Applied", "Applied"),
    ("Received", "Received"),
    ("Shortlisted", "Shortlisted"),
    ("Rejected", "Rejected"),
    ("Selected", "Selected"),
    ("Offered", "Offered"),
]

Organizer_Choices = [("hub", "Hub"), ("chapter", "Chapter"), ("user", "User")]
Event_Status = [("verified", "Verified"), ("pending", "Pending")]
