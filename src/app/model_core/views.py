import os
import json
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from confluent_kafka import Producer

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

    def create(self, request, *args, **kwargs):
        asset_serializer = AssetSerializer(data=request.data)
        model_serializer = ModelTypeSerializer(data=request.data)

        if asset_serializer.is_valid() and model_serializer.is_valid():
            asset = asset_serializer.validated_data["id"]
            model = model_serializer.validated_data["id"]
            user = request.user.id

            msg = json.dumps({"user": user, "asset": asset, "model": model})

            producer = Producer(
                {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER")}
            )

            topic = os.getenv("MODEL_QUEUE_TRAIN_TOPIC")
            producer.produce(topic, msg.encode("utf-8"))
            producer.flush()

            producer.close()

            return Response(
                {"message": "Model training request sent to Kafka"},
                status=status.HTTP_201_CREATED,
            )
