from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsChapterPresidentOrAdmin(BasePermission):
    """
    Only grant permission to resource if one is owner or admin
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_superuser:
            return True

        if (
            request.method == "POST"
            and request.user.groups.filter(name="chapter_president").exists()
        ):
            return True

        return False

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        if obj.chapter.president == request.user or request.user.is_superuser:
            return True

        return False
