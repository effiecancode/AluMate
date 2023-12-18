from rest_framework import serializers

from app.feedback.models import FeedBack

"""
Serializes the FeedBack object.
"""


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = "__all__"
