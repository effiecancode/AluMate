from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):
    chapters = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    feedback = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    hubs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    opportunities = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    news = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
