from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Analytics


class AnalyticsAPIView(APIView):
    def get(self, request):
        analytics_data = Analytics.analyze_data()
        return Response(analytics_data)
