from rest_framework.permissions import BasePermission
from app.constant import UserGroup
from app.chapters.models import Chapter


class IsChapterAdmin(BasePermission):
    """
    Custom permission to allow only chapter admin users to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        result = request.user == obj.chapter_admin
        return result


class IsStaffAdminOrSuperAdmin(BasePermission):
    """
    Custom permission to allow only staff admin and super admin users to perform certain actions.
    """

    def has_permission(self, request, view):
        result = request.user.user_group in [UserGroup.SUPER_ADMIN, UserGroup.STAFF_ADMIN]
        return result


class IsChapterAdminOrStaffAdminOrSuperAdmin(BasePermission):
    """
    Give create, update, or delete permissions to only chapter admin, staff admin, or super admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            chapter_id = view.kwargs.get('pk')
            chapter = Chapter.objects.get(pk=chapter_id)
            result = (
                request.user == chapter.chapter_admin
                or request.user.user_group in [UserGroup.STAFF_ADMIN, UserGroup.SUPER_ADMIN]
            )
            return result
        return False
