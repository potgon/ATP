import os
import json
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from confluent_kafka import Producer, KafkaException

from app.utils.logger import make_log
from app.evaluation_core.serializers import AssetSerializer
from .models import ModelType, TrainedModel
from .serializers import ModelTypeSerializer, TrainedModelSerializer
from .services import delivery_callback


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

            try:
                producer = Producer(
                    {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER")}
                )
            except KafkaException as ke:
                make_log(
                    "KAFKA",
                    30,
                    "kafka_models.log",
                    f"Error creating Kafka producer: {str(ke)}",
                )
                return Response(
                    {"message": "Error sending train request"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            try:
                topic = os.getenv("MODEL_QUEUE_TRAIN_TOPIC")
                producer.produce(
                    topic, msg.encode("utf-8"), callback=delivery_callback()
                )
                producer.flush()

                producer.close()
            except KafkaException as ke:
                make_log(
                    "KAFKA",
                    30,
                    "kafka_models.log",
                    f"Error producing message to topic: {str(ke)}",
                )
                return Response(
                    {"message": "Error sending train request"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": "Model training request sent to Kafka"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Asset/Model could not be validated"},
            status=status.HTTP_400_BAD_REQUEST,
        )
