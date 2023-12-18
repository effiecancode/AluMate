from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class EmailActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.is_active) + str(user.pk) + str(timestamp)


def send_email_confirmation_email(
    receiver_email,
    request: HttpRequest,
    user: get_user_model(),
    app_name="",
    receiver_name="",
    confirmation_url_override=None,
    domain_override=None,
):
    subject = "Confirm your email address"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = EmailActivationTokenGenerator().make_token(user)
    if domain_override is not None:
        domain = domain_override
    else:
        domain = get_current_site(request).domain
    body = render_to_string(
        "email-confirmation-email.html",
        {
            "receiver_name": receiver_name,
            "app_name": app_name,
            "url_override": confirmation_url_override,
            "domain": domain,
            "uidb64": uid,
            "token": token,
        },
    )

    if (
        EmailMessage(
            to=[receiver_email], subject=subject, body=body, reply_to=None
        ).send()
        == 1
    ):
        return True
    else:
        return False


def send_email_confirmation_set_password_email(
    receiver_email,
    request: HttpRequest,
    user: get_user_model(),
    app_name="",
    receiver_name="",
    confirmation_url=None,
):
    subject = "Confirm your email address ad set password"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    email_confirmation_password_set_view_url = reverse(
        "confirm_email_address_set_password",
        kwargs={"uidb64": uid, "token": token},
    )
    if confirmation_url is None:
        confirm_email_url = request.build_absolute_uri(
            email_confirmation_password_set_view_url
        )
    else:
        confirm_email_url = confirmation_url
    body = render_to_string(
        "email-confirmation-email.html",
        {
            "receiver_name": receiver_name,
            "confirm_email_url": confirm_email_url,
            "app_name": app_name,
        },
    )

    if (
        EmailMessage(
            to=[receiver_email], subject=subject, body=body, reply_to=None
        ).send()
        == 1
    ):
        return True
    else:
        return False
