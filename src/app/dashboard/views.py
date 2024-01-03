from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from app.utils.api_utils import get_required_fields
from .serializers import UserSerializer

class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")
    
    def post(self, request, *args, **kwargs):
        req_fields = ["username", "password"]
        try:
            fields = get_required_fields(request, req_fields)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=fields["username"], password=fields["password"]) # Wrap around try-except?
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserView(GenericViewSet, CreateModelMixin):
    serializer = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []
