from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericViewSet

from .models import Algorithm, Asset
from .serializers import AlgorithmSerializer, AssetSerializer

class RunAlgorithmView(GenericViewSet):
    serializer_class = AlgorithmSerializer
    
    @action(details=True, methods=["post"])
    def run(self, request, *args, **kwargs):
        ...

class ListAlgorithmsView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        algorithms = Algorithm.objects.all()
        serializer = AlgorithmSerializer(algorithms, many=True)
        return Response(serializer.data)

class ListAssetsView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
