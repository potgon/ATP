from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Algorithm
from .serializers import AlgorithmSerializer

class ListAlgorithmsView(APIView):
    def get(self, request, *args, **kwargs):
        algorithms = Algorithm.objects.all()
        serializer = AlgorithmSerializer(algorithms, many=True)
        return Response(serializer.data)