from rest_framework import serializers

from .models import Hub, HubRegister, HubLeadership


class HubLeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubLeadership
        fields = "__all__"


class HubSerializer(serializers.ModelSerializer):
    hub_leaders = HubLeadershipSerializer(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Hub
        fields = (
            "id",
            "name",
            "hub_profile_image",
            "description",
            "members",
            "created_on",
            "hub_admin",
            "hub_leaders",
        )


class HubRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubRegister
        fields = "__all__"
