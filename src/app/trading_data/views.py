from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Position
from .fetcher import Fetcher
from .serializers import ClosePositionSerializer

class ClosePositionViewSet(GenericViewSet, UpdateModelMixin):
    queryset = Position.objects.all()
    serializer_class = ClosePositionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response({"message": "Position closed successfully"}, status=status.HTTP_202_ACCEPTED)
