from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from app.user_module.serializers import UserSerializer

from .filters import UserProfileInsightFilter

User = get_user_model()


class AlumniInsights(GenericAPIView):
    queryset = User.objects.all()
    pagination_class = None
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserProfileInsightFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
