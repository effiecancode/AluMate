from rest_framework import viewsets

from .models import FeedBack
from .serializer import FeedBackSerializer

"""
Adds a ViewSet for our FeedBack Object.
"""


class FeedBackViewSet(viewsets.ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
