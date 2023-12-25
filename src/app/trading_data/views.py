from rest_framework.views import APIView
from rest_framework.response import Response

class OpenPositionView(APIView):
    def post(self, request, *args, **kwargs):
        algo_name = request.data.get("algo_name")
        ticker = request.data.get("ticker")
        