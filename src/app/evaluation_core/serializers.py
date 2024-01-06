from rest_framework import serializers
from .models import Algorithm, Asset

class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'
        
        def validate_algo(self, data):
            if not Algorithm.objects.filter(name=data["algo_name"], status="Active").exists():
                raise serializers.ValidationError("Algorithm is not currently operative")
        
        return data

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
