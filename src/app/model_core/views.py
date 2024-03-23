from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import ModelType, TrainedModel
from .serializers import ModelTypeSerializer, TrainedModelSerializer


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
