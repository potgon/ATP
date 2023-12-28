from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import manage_algorithm
from .exceptions import DuplicateAssetException
from app.evaluation_core.models import Algorithm
from .models import Position
from .broker import Broker

class OpenPositionView(APIView):
    def post(self, request, *args, **kwargs):
        algo_name = request.data.get("algo_name")
        ticker = request.data.get("ticker")
        
        if not algo_name:
            return Response({"error":"Missing algorithm"}, status=status.HTTP_400_BAD_REQUEST)
        if not ticker:
            return Response({"error":"Missing ticker"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Algorithm.objects.get(name=algo_name)
        except Algorithm.DoesNotExist:
            return Response({"error":"Algorithm does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Algorithm.objects.get(name=algo_name).status == "Active":
            return Response({"error":"Algorithm is not currently operative"})
        
        try:
            manage_algorithm.delay(algo_name, ticker, Broker())
        except DuplicateAssetException as e:
            return Response({"error":str(e)}, status=status.HTTP_409_CONFLICT)
        
        return Response({"message":f"{algo_name} algorithm successfully started for {ticker}"}, status=status.HTTP_202_ACCEPTED)
    
class ClosePositionView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            pos = Position.objects.get(id=request.data.get("id"))
        except Position.DoesNotExist:
            return Response({"error":"Position not found"},status=status.HTTP_400_BAD_REQUEST)
        try:
            Broker().close_pos(pos)
        except Exception: # Broker's exception if position couldn't be closed
            return Response({"error":"Position couldn't be closed"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"Position closed successfully"}, status=status.HTTP_202_ACCEPTED)
        