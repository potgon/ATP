from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.evaluation_core.serializers import AssetSerializer
from .models import ModelType, TrainedModel
from .serializers import ModelTypeSerializer, TrainedModelSerializer
from .trainer import Trainer


class ListModelTypeView(GenericViewSet, ListModelMixin):
    queryset = ModelType.objects.all()
    serializer_class = ModelTypeSerializer

    def list(self, request, *args, **kwargs):
        return super(ListModelTypeView, self).list(request, *args, **kwargs)


class ListTrainedModelsView(GenericViewSet, ListModelMixin):
    queryset = TrainedModel
    serializer_class = TrainedModelSerializer

    def list(self, request, *args, **kwargs):
        return super(ListTrainedModelsView, self).list(request, *args, **kwargs)

class TrainModelView(GenericViewSet, CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        asset_serializer = AssetSerializer(data=request.data)
        model_serializer = ModelTypeSerializer(data=request.data)
        
        if asset_serializer.is_valid() and model_serializer.is_valid():
            asset = asset_serializer.validated_data["ticker"]
            model = model_serializer.validated_data["model_name"]
            user = request.user
            
            