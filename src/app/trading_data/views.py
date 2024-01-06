from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .tasks import manage_request, schedule_algo
from app.evaluation_core.models import Algorithm, Asset
from .models import Position
from .fetcher import Fetcher
from .serializers import ClosePositionSerializer
from app.utils.api_utils import get_required_fields

class ClosePositionViewSet(GenericViewSet):
    @action(detail=True, methods=["post"])
    def close(self, request, *args, **kwargs):  
        serializer = ClosePositionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            position = serializer.validated_data['pos_id']
            try:
                serializer.update(position, validated_data=serializer.validated_data)
            except TypeError as e:
                return Response({"error":str(e)})    
            return Response({"message": "Position closed successfully"}, status=status.HTTP_202_ACCEPTED)
