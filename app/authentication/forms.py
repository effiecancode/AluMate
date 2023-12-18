from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

UserModel = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    def save(
        self,
        domain_override=None,
        subject_template_name="password-reset-subject.txt",
        email_template_name="password-reset-email.html",
        use_https=False,
        token_generator=PasswordResetTokenGenerator(),
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
        app_name="",
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            domain = current_site.domain
        else:
            domain = domain_override

        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "app_name": app_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class PasswordSetForm(forms.Form):
    password = forms.CharField(
        required=True, min_length=8, widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        required=True, min_length=8, widget=forms.PasswordInput()
    )

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error(
                field="password", error="The passwords provided did not match."
            )
        else:
            return super().clean()
