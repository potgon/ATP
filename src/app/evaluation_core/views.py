from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Algorithm, Asset
from .serializers import AlgorithmSerializer, AssetSerializer

class ListAlgorithmsView(APIView):
    def get(self, request, *args, **kwargs):
        algorithms = Algorithm.objects.all()
        serializer = AlgorithmSerializer(algorithms, many=True)
        return Response(serializer.data)
    
class ListAssetsView(APIView):
    def get(self, request, *args, **kwargs):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)