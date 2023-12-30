from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import manage_request, schedule_algo
from .exceptions import DuplicateAssetException
from app.evaluation_core.models import Algorithm, Asset
from .models import Position
from .broker import Broker
from .fetcher import Fetcher
from app.utils.db_utils import retrieve_single_record, retrieve_multiple_records
from app.utils.api_utils import get_required_fields

class OpenPositionView(APIView):
    def post(self, request, *args, **kwargs):
        req_fields = ["algo_name", "ticker", "user"] # Check user auth
        try:
            fields = get_required_fields(request, req_fields) 
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if not retrieve_record(Algorithm, 1, name=fields["algo_name"]).status == "Active":
            return Response({"error":"Algorithm is not currently operative"})

        try:
            manage_request(fields["algo_name"], fields["ticker"])
        except DuplicateAssetException as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_409_CONFLICT)

        if retrieve_multiple_records(Position, 0, user_id=fields["user"], asset_id=retrieve_single_record(Asset, 1, ticker=fields["ticker"]), status=StatusChoices.OPEN):        
            return Response({"error":"An open position already exists for this asset"}, status=status.HTTP_400_BAD_REQUEST)

        schedule_algo.delay(fields["algo_name"], fields["ticker"], Broker())
        return Response({"message":f"{fields['algo_name']} algorithm successfully started for {fields['ticker']}"}, status=status.HTTP_202_ACCEPTED)

class ClosePositionView(APIView):
    def delete(self, request, *args, **kwargs):
        req_fields = ["pos_id", "user_id"]
        try:
            fields = get_required_fields(request, req_fields)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        pos = retrieve_single_record(Position, 1, id=fields["pos_id"], user_id=fields["user_id"])
        try:
            Broker().close_pos(pos)
        except Exception: # Broker's exception if position couldn't be closed
            return Response({"error":"Position couldn't be closed"},status=status.HTTP_400_BAD_REQUEST)
        try:
            exit_price = Fetcher.get_latest_close(retrieve_single_record(Asset, 1, id=pos.asset).ticker)
        except Exception as e:
            return Response({"error":"Failed to retrieve exit price for current asset"})
        pos.close_db(exit_price)

        return Response({"message":"Position closed successfully"}, status=status.HTTP_202_ACCEPTED)
