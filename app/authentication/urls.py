from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    EmailActivationManager,
    MyTokenObtainPairView,
    PasswordChangeManager,
    PasswordResetRequestManager,
    confirm_email_address_set_password,
    resend_confirmation_email,
)

urlpatterns = [
    path("user/sign-in/", MyTokenObtainPairView.as_view(), name="sign-in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "change-password",
        PasswordChangeManager.as_view(),
        name="password_change",
    ),
    path(
        "confirm-email/",
        EmailActivationManager.as_view(),
        name="email_confirmation",
    ),
    path(
        "resend-confirmation-email/<uidb64>/",
        resend_confirmation_email,
        name="resend_confirmation_email",
    ),
    path(
        "confirm-email-set-password/<uidb64>/<token>/",
        confirm_email_address_set_password,
        name="confirm_email_address_set_password",
    ),
    path(
        "reset-password/",
        PasswordResetRequestManager.as_view(),
        name="password_reset_request",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="reset-password.html"),
        name="password_reset_confirm",
    ),
    # path(
    #     "reset-password/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    path(
        "reset-password/done/",
        PasswordResetCompleteView.as_view(
            template_name="password-reset-done.html"
        ),
        name="password_reset_complete",
    ),
]
