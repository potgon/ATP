from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .tasks import manage_request, schedule_algo
from app.evaluation_core.models import Algorithm, Asset
from .models import Position
from .broker import Broker
from .fetcher import Fetcher
from .serializers import OpenPositionSerializer, ClosePositionSerializer
   

class OpenPositionView(GenericViewSet, CreateModelMixin):
    serializer_class = OpenPositionSerializer
    
    def create(self, serializer):
        algo_name = serializer.validated_data["algo_name"].upper()
        ticker = serializer.validated_data["ticker"]
        manage_request(algo_name, ticker)
        schedule_algo.delay(algo_name, ticker, Broker())

class ClosePositionView(APIView):
    serializer_class = ClosePositionSerializer
    
    @action(detail=True, methods=["post"])
    def close(self, request, *args, **kwargs):
        serializer = ClosePositionSerializer(data=request.data)
        if serializer.is_valid():
            pos = Position
