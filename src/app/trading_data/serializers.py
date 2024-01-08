from rest_framework import serializers

from .models import Position
from .fetcher import get_latest_result
from app.evaluation_core.models import Algorithm, Asset

class ClosePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '[id]'

    def validate_pos_id(self, pos_id):
        try:
            position = Position.objects.get(id=pos_id, user_id=self.context['request'].user.id)
        except Position.DoesNotExist:
            raise serializers.ValidationError("Position does not exist or you do not have permission to close it")
        return position

    def update(self, instance, validated_data):
        if isinstance(instance, Position):
            instance.close_db(get_latest_result(ticker=instance.asset.ticker), column="Close")
            return instance
        else:
            raise TypeError("Expected a Position instance")
