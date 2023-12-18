from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ValidationError
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app.authentication.serializers import MyTokenObtainPairSerializer

from .email_confirmation import (
    EmailActivationTokenGenerator,
    send_email_confirmation_email,
)
from .forms import (
    CustomPasswordResetForm,
    PasswordSetForm,
)

UserModel = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):  # type: ignore
    serializer_class = MyTokenObtainPairSerializer


def resend_confirmation_email(request, uidb64):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), id=uid)

    if send_email_confirmation_email(
        request=request,
        user=user,
        receiver_email=user.email,
        receiver_name=f"{user.first_name} {user.last_name}",
        app_name="ELP Portal",
    ):
        context = {
            "page_title": "Confirmation email",
            "message_title": "Success!!",
            "message_content": "A confirmation email has been sent.",
        }

    else:
        context = {
            "page_title": "Confirmation email",
            "message_title": "Oops!!",
            "message_content": "Sorry we were unable to send confirmation "
            "email.",
        }

    return render(request, "message-page.html", context)


class EmailActivationManager(APIView):
    def get(self, request):
        uidb64 = request.GET.get("uidb64")
        token = request.GET.get("token")

        if uidb64 is None or token is None:
            context = {
                "status": "error",
                "page_title": "Invalid link",
                "message_title": "Oops!!",
                "message_content": "The link you clicked is invalid.",
            }

            return render(request, "message-page.html", context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), id=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
            Exception,
        ):
            context = {
                "status": "error",
                "page_title": "Invalid link",
                "message_title": "Oops!!",
                "message_content": "The link you clicked is invalid.",
            }

            return render(request, "message-page.html", context)
        confirmed = False

        if EmailActivationTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            confirmed = True

        context = {
            "is_active": user.is_active,
            "uidb64": uidb64,
            "confirmed": confirmed,
        }
        return render(
            request,
            "email-activation-result.html",
            context,
        )

    def post(self, request):
        try:
            errors = {}

            action = request.data.get("action")
            if action is None or action == "":
                errors = {**errors, "action": ["This value is required"]}

            uidb64 = request.data.get("uidb64")
            if uidb64 is None or uidb64 == "":
                errors = {**errors, "uidb64": ["This value is required"]}

            token = request.data.get("token")
            if token is None or token == "":
                errors = {**errors, "token": ["This value is required"]}

            if len(errors) > 0:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"errors": errors}
                )

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=uid)

            if action == "confirm":
                if EmailActivationTokenGenerator().check_token(user, token):
                    user.is_active = True
                    user.save()
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "messages": {
                                "detail": "Email address confirmed "
                                "successfully"
                            }
                        },
                    )

                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "errors": {
                                "detail": "Invalid link, It could be that "
                                "the confirmation link has already "
                                "make been used or the link has expired."
                            },
                            "data": {
                                "uidb64": uidb64,
                                "user_account_active": user.is_active,
                            },
                        },
                    )

            elif action == "resend-email":
                if send_email_confirmation_email(
                    request=request,
                    user=user,
                    receiver_email=user.email,
                    receiver_name=f"{user.first_name} {user.last_name}",
                    app_name="App in App",
                ):
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "messages": {
                                "detail": "Confirmation email sent "
                                "successfully"
                            }
                        },
                    )

                else:
                    return Response(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={
                            "errors": {
                                "detail": "Confirmation email sending failed"
                            }
                        },
                    )

            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"errors": {"action": "Invalid action"}},
                )

        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "errors": {
                        "uidb64": "User with the given id does not exist"
                    }
                },
            )

        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )


def confirm_email_address_set_password(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), id=uid)

    if PasswordResetTokenGenerator().check_token(user, token):
        if request.method == "GET":
            form = PasswordSetForm()

            context = {
                "form": form,
                "title": "Set a new password",
            }
            return render(request, "password-set.html", context)

        elif request.method == "POST":
            filled_form = PasswordSetForm(request.POST)

            if filled_form.is_valid():
                user.set_password(filled_form.cleaned_data["password"])
                user.is_active = True
                user.save()

                context = {
                    "page_title": "Set password",
                    "message_title": "Success!!",
                    "message_content": "Your password has been set "
                    "successfully, you can now log in to "
                    "your account.",
                }

                return render(
                    request,
                    "message-page.html",
                    context,
                )

            else:
                form = filled_form
                context = {
                    "form": form,
                    "title": "Set a new password",
                }

                return render(
                    request,
                    "set-password.html",
                    context,
                )

    context = {
        "page_title": "Set password",
        "message_title": "Oops!!",
        "message_content": "The link you clicked is invalid, it may be that "
        "the link has already been used or has"
        "expired. Please contact your admin to resend an activation link",
    }

    return render(request, "message-page.html", context)


class PasswordResetRequestManager(APIView):
    def post(self, request):
        try:
            form = CustomPasswordResetForm(request.data)
            if form.is_valid():
                form.save(
                    domain_override=get_current_site(request).domain,
                    app_name="ELP Portal",
                )

                return Response(
                    {
                        "messages": {
                            "detail": "If an account with that email exists, you will receive an "
                            "email with further instructions to reset your password"
                        }
                    }
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"errors": form.errors},
                )

        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )


class PasswordChangeManager(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password", None)
        new_password1 = request.data.get("new_password1", None)
        new_password2 = request.data.get("new_password2", None)

        if not (old_password and new_password1 and new_password2):
            return Response({"error": "All fields are required."}, status=400)

        if not check_password(old_password, user.password):
            return Response(
                {"error": "Old password is incorrect."}, status=400
            )

        if new_password1 != new_password2:
            return Response({"error": "Passwords do not match."}, status=400)

        # Update the user's password
        user.set_password(new_password1)
        user.save()

        return Response({"message": "Password reset successful."}, status=200)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )
