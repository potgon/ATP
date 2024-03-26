from rest_framework import serializers

from .models import ModelType, TrainedModel


class ModelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelType
        fields = "__all__"

    def validate(self, data):
        if not ModelType.objects.filter(
            name=data["model_name"], status="Active"
        ).exists():
            raise serializers.ValidationError("Model type is not currently operative")

        return data


class TrainedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedModel
        fields = "__all__"

    def validate(self, data):
        if not TrainedModel.objects.filter(
            name=data["model_name"], status="Active"
        ).exists():
            raise serializers.ValidationError("Model is not currently operative")

        return data
