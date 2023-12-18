from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

from app.constant import UserGroup


class IsHubAdmin(BasePermission):
    """
    Custom permission to allow only hub admin users to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view that the user is trying to access.
            obj: The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user == obj.chapter_admin


class HubPermissions(IsAuthenticated):
    """
    Custom permission to allow only admin users to create hubs.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view that the user is trying to access.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.user.user_group in [
            UserGroup.SUPER_ADMIN,
            UserGroup.STAFF_ADMIN,
        ]:
            return True
        return False
