from rest_framework import serializers

from app.dashboard.models import User
from .models import Algorithm, Asset


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = "__all__"

    def validate(self, data):
        if not Algorithm.objects.filter(
            name=data["algo_name"], status="Active"
        ).exists():
            raise serializers.ValidationError(
                "Algorithm is not currently operative")

        return data


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

    def validate(self, data):
        if (
            not Asset.objects.filter(name=data["name"])
            or Asset.objects.filter(ticker=data["ticker"]).exists()
        ):
            raise serializers.ValidationError("Asset does not exist")
        return data


class RunAlgorithmSerializer(AlgorithmSerializer):
    name = serializers.CharField(required=True, max_length=30)

    def validate(self, data):
        data = super().validate(data)
        try:
            User.objects.get(id=self.context["request"].user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Logged user is required to run an algorithm"
            )
        try:
            Asset.objects.get(name=data["name"])
        except Asset.DoesNotExist:
            raise serializers.ValidationError(
                "Asset does not exist or is not currently supported"
            )
        return data
