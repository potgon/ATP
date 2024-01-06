from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework import status
from rest_framework.decorators import action

from .models import Algorithm, Asset
from .serializers import AlgorithmSerializer, AssetSerializer
from app.trading_data_broker import Broker
from app.trading_data.tasks import manage_request, schedule_algo
from app.utils.api_utils import get_required_fields

class RunAlgorithmView(GenericViewSet):    
    @action(details=True, methods=["post"])
    def run(self, request, *args, **kwargs):
        try:
            fields = get_required_fields(request, ["algo_name", "ticker"])
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = AlgorithmSerializer(Algorithm.objects.get(name=fields["algo_name"]), data=request.data)
            if serializer.is_valid(raise_exception=True):
                manage_request(fields["algo_name"], fields["ticker"])
                schedule_algo.delay(fields["algo_name"], fields["ticker"], Broker())
                return Response({"message":f"{fields['algo_name']} started successfully"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Algorithm.DoesNotExist:
            return Response({"error":"Algorithm not found"}, status=status.HTTP_404_NOT_FOUND)

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
