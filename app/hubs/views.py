from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from .models import (
    Hub,
    HubRegister,
    HubLeadership
)
from .permissions import (
    HubPermissions,
    IsHubAdmin,
)
from .serializers import (
    HubRegisterSerializer,
    HubSerializer,
    HubLeadershipSerializer,
)
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.views import APIView

User = get_user_model()


class HubViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for hubs.
    """

    queryset = Hub.objects.all()
    serializer_class = HubSerializer

    def get_permissions(self):
        """
        Permissions.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permissions = [IsAuthenticated, HubPermissions]
            if self.action == "update":
                permissions.append(IsHubAdmin)
            return [permission() for permission in permissions]
        elif self.action == "list":
            permissions = [IsAuthenticated]
            return [permission() for permission in permissions]
        return []

    def perform_create(self, serializer):
        """
        Override perform_create to provide custom behavior during hub creation.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Override perform_update to provide custom behavior during hub update.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Override perform_destroy to provide custom behavior during hub deletion.
        """
        instance.delete()


class HubLeadershipCreateView(CreateAPIView):
    serializer_class = HubLeadershipSerializer
    queryset = HubLeadership.objects.all()
    permission_classes = [IsAuthenticated]


class HubLeadershipUpdateView(APIView):
    def put(self, request, hub_id, user_id, format=None):
        try:
            hub = hub.objects.get(id=hub_id)
            user = User.objects.get(id=user_id)
        except hub.DoesNotExist:
            return JsonResponse(
                {"error": "hub not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            hub_leadership = HubLeadership.objects.get(id=hub_id)
        except HubLeadership.DoesNotExist:
            return JsonResponse(
                {"error": "hub Leadership not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = HubLeadershipSerializer(
            hub_leadership, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "hub Leadership updated successfully",
                    "data": serializer.data,
                }
            )
        else:
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class HubLeadershipListView(ListAPIView):
    serializer_class = HubLeadershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hub_id = self.kwargs.get("hub_id")
        return HubLeadership.objects.filter(hub_id=hub_id)


class HubRegisterListCreateView(generics.ListCreateAPIView):
    """
    List and create hub registrations.
    """

    queryset = HubRegister.objects.all()
    serializer_class = HubRegisterSerializer
    permission_classes = [HubPermissions]

    def perform_create(self, serializer):
        """Override perform_create to provide custom behavior during hub registration creation."""
        serializer.save()


class HubRegisterRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, and delete hub registration.
    """

    queryset = HubRegister.objects.all()
    serializer_class = HubRegisterSerializer
    permission_classes = [HubPermissions, IsHubAdmin]

    def get(self, request, *args, **kwargs):
        """Handle GET requests and retrieve a specific hub registration."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handle PUT requests and update the details of a specific hub registration."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests and update the details of a specific hub registration."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests and delete a specific hub registration."""
        return self.destroy(request, *args, **kwargs)
