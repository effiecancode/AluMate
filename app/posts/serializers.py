"""
Serializer Module for the Post and Like models.

Serializer for the Post model: All Fields a serialized.
Serializer for the Like model: All Fields a serialized.

Returns:
    A serializer object for the Post and Like models.
"""

from rest_framework import serializers
from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
