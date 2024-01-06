from rest_framework import serializers

from .models import Position
from app.evaluation_core.models import Algorithm, Asset

class OpenPositionSerializer(serializers.Serializer):
    algo_name = serializers.CharField(max_length=100)
    ticker = serializers.CharField(max_length=10)
    user = serializers.IntegerField()
    
    def validate_algo(self, data):
        if not Algorithm.objects.filter(name=data["algo_name"], status="Active").exists():
            raise serializers.ValidationError("Algorithm is not currently operative")
        
        if Position.objects.filter(user_id=data["user"], asset_ticker=data["ticker"], status="Open").exists():
            raise serializers.ValidationError("An open position already exists for this asset")
        
        return data
    
    def create(self, validated_data):
        position = Position(user_id=validated_data["user"],
                            asset=Asset.objects.get(ticker=validated_data["ticker"]),
                            algorithm=Algorithm.objects.get(name=validated_data["algo_name"]))
        return position

class ClosePositionSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    def validate(self, data):
        try:
            position = Position.objects.get(id=data["pos_id"], user_id=data["user_id"])
        except Position.DoesNotExist:
            raise serializers.ValidationError("Position does not exist or you do not have permission to close it")
        return data