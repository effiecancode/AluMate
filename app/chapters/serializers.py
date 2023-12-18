from rest_framework import serializers

from .models import (
    Chapter,
    ChapterRegister,
    ChapterLeadership
)


class ChapterLeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterLeadership
        fields = "__all__"

class ChapterSerializer(serializers.ModelSerializer):
    chapter_leaders = ChapterLeadershipSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Chapter
        fields = (
            "id",
            "name",
            "chapter_profile_image",
            "institution",
            "registration_fee",
            "description",
            "members",
            "created_on",
            "chapter_admin",
            "chapter_leaders",
        )


class ChapterRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterRegister
        fields = "__all__"
