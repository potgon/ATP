from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import manage_algorithm
from .exceptions import DuplicateAssetException
from app.evaluation_core.models import Algorithm

class OpenPositionView(APIView):
    def post(self, request, *args, **kwargs):
        algo_name = request.data.get("algo_name")
        ticker = request.data.get("ticker")
        
        if not algo_name:
            return Response({"error":"Missing algorithm"}, status=status.HTTP_400_BAD_REQUEST)
        if not ticker:
            return Response({"error":"Missing ticker"}, status=status.HTTP_400_BAD_REQUEST)
        if not Algorithm.objects.filter(name=algo_name).exists():
            return Response({"error":"Algorithm does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not Algorithm.objects.get(name=algo_name).status == "Active":
            return Response({"error":"Algorithm is not currently operative"})
        
        try:
            manage_algorithm.delay(algo_name, ticker)
        except DuplicateAssetException as e:
            return Response({"error":str(e)}, status=status.HTTP_409_CONFLICT)
        
        return Response({"message":f"{algo_name} algorithm successfully started for {ticker}"}, status=status.HTTP_202_ACCEPTED)