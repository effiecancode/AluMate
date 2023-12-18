from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class UnlikeView(generics.UpdateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def update(self, request, *args, **kwargs):
        """
        update: Allows a user to toggle the like button.

        It must first verify if the user is the owner of the like.
        """
        try:
            like_instance = self.get_queryset().get(pk=kwargs['pk'])
        except Like.DoesNotExist:
            return Response(
                {"message": "Like not found."},
                status=status.HTTP_404_NOT_FOUND)

        if like_instance.user == request.user:
            like_instance.is_liked = not like_instance.is_liked
            like_instance.save()
            return Response(
                {"message": "Like status updated successfully."},
                status=status.HTTP_200_OK)

        return Response(
            {"message": "You are not authorized to unlike this content."},
            status=status.HTTP_403_FORBIDDEN)
