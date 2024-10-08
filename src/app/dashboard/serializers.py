from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from app.dashboard.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "priority",
        )

    def validate_password(self, value):
        if len(value) < 5:
            raise Exception
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)
