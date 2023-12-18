from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.chapters.models import Chapter, ChapterRegister, ChapterLeadership
from .serializers import (
    ChapterSerializer,
    ChapterRegisterSerializer,
    ChapterLeadershipSerializer,
)
from app.caching_mixins import CacheMixin
from .permissions import IsChapterAdminOrStaffAdminOrSuperAdmin
from rest_framework.decorators import action

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)

from rest_framework.views import APIView

User = get_user_model()


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    # @CacheMixin.cache_view
    @action(
        detail=True,
        methods=["PUT"],
        permission_classes=[IsChapterAdminOrStaffAdminOrSuperAdmin],
    )
    def update_chapter(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # @CacheMixin.cache_view
    @action(
        detail=True,
        methods=["DELETE"],
        permission_classes=[IsChapterAdminOrStaffAdminOrSuperAdmin],
    )
    def delete_chapter(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_permissions(self):
    #     if self.action in ["create", "update_chapter", "delete_chapter"]:
    #         permission_classes = [IsChapterAdminOrStaffAdminOrSuperAdmin]
    #     elif self.action == "retrieve":
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = []
    #     return [permission() for permission in permission_classes]


class ChapterLeadershipCreateView(CreateAPIView):
    serializer_class = ChapterLeadershipSerializer
    queryset = ChapterLeadership.objects.all()
    permission_classes = [IsAuthenticated]


class ChapterLeadershipUpdateView(APIView):
    def put(self, request, chapter_id, user_id, format=None):
        try:
            chapter = Chapter.objects.get(id=chapter_id)
            user = User.objects.get(id=user_id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "Chapter not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            chapter_leadership = ChapterLeadership.objects.get(id=chapter_id)
        except ChapterLeadership.DoesNotExist:
            return Response(
                {"error": "Chapter Leadership not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ChapterLeadershipSerializer(
            chapter_leadership, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Chapter Leadership updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ChapterLeadershipListView(ListAPIView):
    serializer_class = ChapterLeadershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chapter_id = self.kwargs.get("chapter_id")
        return ChapterLeadership.objects.filter(chapter_id=chapter_id)


class SearchChapter(generics.ListAPIView):
    serializer_class = ChapterSerializer

    # @CacheMixin.cache_view
    def get_queryset(self):
        """
        Returns a queryset of chapters filtered by name.

        Returns:
            queryset: A queryset of chapters filtered by name.
        """
        pass
        query = self.kwargs["chapter_name"]
        return Chapter.objects.filter(name__icontains=query)


class ChapterRegistrationView(generics.CreateAPIView):
    """Register user to a chapter"""

    serializer_class = ChapterRegisterSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        # User already registered to a chapter??
        existing_registration = ChapterRegister.objects.filter(
            user=user
        ).first()
        if existing_registration:
            return Response(
                {
                    "error": f"User is Member of '{existing_registration.chapter.name}'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        chapter_id = self.kwargs.get("chapter_id")
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "Chapter not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chapter=chapter, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Caching APIs
class CachedChapterListView(ChapterViewSet):
    cache_list = CacheMixin().cache_view(ChapterViewSet.list)

class CachedChapterDetailView(ChapterViewSet):
    cache_retrieve = CacheMixin().cache_view(ChapterViewSet.retrieve)

class CachedChapterLeadershipListView(ChapterLeadershipListView):
    cache_list = CacheMixin().cache_view(ChapterLeadershipListView.list)

class CachedSearchChapterView(SearchChapter):
    cache_list = CacheMixin().cache_view(SearchChapter.list)

class CachedChapterRegistrationView(ChapterRegistrationView):
    cache_create = CacheMixin().cache_view(ChapterRegistrationView.create)
