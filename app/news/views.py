from rest_framework import viewsets
from rest_framework.response import Response

from app.constant import UserGroup

from .models import (
    Comment,
    Like,
    Post,
)
from .serializers import (
    CommentSerializer,
    LikeSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(visible=True)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            user_group = request.user.user_group
        except AttributeError:
            return Response(
                {"error": "User information not available"},
                status=400,
            )

        try:
            if (
                user_group == UserGroup.SUPER_ADMIN
                or user_group == UserGroup.STAFF_ADMIN
            ):
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response(
                    {"error": "You are not authorized to create posts"},
                    status=403,
                )
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {e}"},
                status=500,
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.queryset.filter(post__visible=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        return self.queryset.filter(post__visible=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
