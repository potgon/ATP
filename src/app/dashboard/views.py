from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from app.utils.api_utils import get_required_fields

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
    
class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html")
    
    def post(self, request, *args, **kwargs):
        req_fields = ["username, email, first_name, second_name, password"]
        try:
            fields = get_required_fields(request, req_fields)
        except Exception as e:
            return Response({"error":str(e)}, status=HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=fields["username"]).exists():
            return Response({"error":"Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.create(username=fields["username"], email=fields["email"], first_name=fields["first_name"], second_name=fields["second_name"], password=make_password(fields["password"])):
            return Response({"message":"User created successfully"}, status=HTTP_201_CREATED)
        return Response({"error":"User creation failed"}) # Log failure info
