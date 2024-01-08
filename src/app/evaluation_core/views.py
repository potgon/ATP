from rest_framework.response import Response
from rest_framework.generics import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework import status
from rest_framework.decorators import action

from .models import Algorithm, Asset
from .serializers import AlgorithmSerializer, AssetSerializer
from app.trading_data_broker import Broker
from app.trading_data.tasks import manage_request, schedule_algo

class RunAlgorithmView(GenericViewSet):    
    @action(details=True, methods=["post"])
    def run(self, request, *args, **kwargs):
        serializer = AlgorithmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            manage_request(serializer.validated_data.get("algo_name"), serializer.validated_data.get("ticker"))
            schedule_algo.delay(serializer.validated_data.get("algo_name"), serializer.validated_data.get("ticker"), Broker())
            return Response({"message":f"{serializer.validated_data.get('algo_name')} started successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListAlgorithmsView(GenericViewSet, ListModelMixin):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer
    
    def list(self, request, *args, **kwargs):
        return super(ListAlgorithmsView, self).list(request, *args, **kwargs)

class ListAssetsView(GenericViewSet, ListModelMixin):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    def list(self, request, *args, **kwargs):
        return super(ListAssetsView, self).list(request, *args, **kwargs)
