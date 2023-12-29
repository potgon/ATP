from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import manage_request, schedule_algo
from .exceptions import DuplicateAssetException
from app.evaluation_core.models import Algorithm, Asset
from .models import Position
from .broker import Broker
from app.utils.db_utils import retrieve_single_record, retrieve_multiple_records

class OpenPositionView(APIView):
    def post(self, request, *args, **kwargs):
        algo_name = request.data.get("algo_name")
        ticker = request.data.get("ticker")
        user = request.data.get("user") # Change to whatever method I'll use to auth
        
        if not algo_name:
            return Response({"error":"Missing algorithm"}, status=status.HTTP_400_BAD_REQUEST)
        if not ticker:
            return Response({"error":"Missing ticker"}, status=status.HTTP_400_BAD_REQUEST)
        if not retrieve_record(Algorithm, name=algo_name).status == "Active":
            return Response({"error":"Algorithm is not currently operative"})
        
        try:
            manage_request(algo_name, ticker)
        except DuplicateAssetException as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_409_CONFLICT)
        
        if retrieve_multiple_records(Position, user_id=user, asset_id=retrieve_single_record(Asset, ticker=ticker), status=StatusChoices.OPEN):        
            return Response({"error":"An open position already exists for this asset"}, status=status.HTTP_400_BAD_REQUEST)
            
        schedule_algo.delay(algo_name, ticker, Broker())
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
        