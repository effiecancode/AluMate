import re

from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    response,
    status,
    viewsets,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response

from app.constant import UserGroup
from app.opportunities.models import (
    Department,
    Opportunity,
    OpportunityApplication,
)

from .serializers import (
    DepartmentSerializer,
    OpportunityApplicationSerializer,
    OpportunitySerializer,
)


class UserWriteOpportunityPermission(BasePermission):
    """
    Permits only Opportunity authors to edit its specs
    """

    message = "Editing an opportunity is restricted to the creator only"

    def has_object_permission(
        self, request, view, obj
    ) -> (
        bool
    ):  # checks if current user posted the opportunity or the request method is applied
        return request.method in SAFE_METHODS or request.user == obj.posted_by


class OpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()

    default_permission_classes = []

    # only admin can create opportunities with user group 400 and 500
    def create(self, request, *args, **kwargs):
        try:
            user_group = request.user.user_group
        except AttributeError:
            return Response(
                {"error": "User information not available"},
                status=400,
            )

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
                {"error": "You are not authorized to create opportunities"},
                status=403,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            user_group = request.user.user_group
        except AttributeError:
            return Response(
                {"error": "User information not available"},
                status=400,
            )

        if (
            user_group == UserGroup.SUPER_ADMIN
            or user_group == UserGroup.STAFF_ADMIN
        ):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {
                    "detail": f"Opportunity with ID {instance.id} deleted successfully."
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You are not authorized to delete opportunities"},
                status=403,
            )

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return self.default_permission_classes


class OpportunityApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunityApplicationSerializer
    queryset = OpportunityApplication.objects.all()
    # TODO: Uncomment me in production
    # permission_classes = (
    #     IsAuthenticated,
    #     IsAdminUser,
    # )

    def get_queryset(self, **kwargs):
        query_set = OpportunityApplication.objects.all()
        #  search and filter opportunities
        self.search_fields = ["user", "opportunity"]  # based on these fields
        self.filter_backends = (filters.SearchFilter,)
        return query_set

    def get_object(self, queryset=None, **kwargs):
        # self.permission_classes =[UserWriteOpportunityPermission]  # TODO: Uncomment me in production
        return get_object_or_404(
            OpportunityApplication, id=self.kwargs.get("pk")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            form_data = dict(request.data)
            for key in form_data:
                if not key == "csrfmiddlewaretoken":
                    self.strip_html("".join(form_data.get(key)), sub=False)
            return super().update(request, *args, **kwargs)
        except ValueError as e:
            return response.Response(
                f"{e}", status=status.HTTP_400_BAD_REQUEST
            )

    def strip_html(self, text: str, sub=True) -> str:
        """
        checks for html tags and either strips them or raises a value error depending on the sub param value

        :param text {str} - the string data to be searched against
        :param sub? {bool} - an optional flag that decides whether the tags are stripped or not
        :returns {str | ValueError}
        """

        if sub:
            return re.sub(
                r"%3C.*?%3E", "", re.sub(r"<.*?>", "", text)
            )  # strip tags off
        if re.search(r"%3C.*?%3E", text) or re.search(r"<.*?>", text):
            raise ValueError(
                "HTML tags and entities are not allowed"
            )  # raise value error if tags are found
        return text


class OpportunityDetail(RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    # TODO: Uncomment me in production
    # permission_classes = [UserWriteOpportunityPermission]


class DepartmentCrudViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def createDepartment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class DepartmentList(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # TODO: Uncomment me in production
    # permission_classes = (
    #     IsAuthenticated,
    #     IsAdminUser,
    # )

    def perform_create(self, serializer):
        serializer.save()
