from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from app.utils.api_utils import get_required_fields
from .serializers import UserSerializer
    
class RegisterUserView(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []
    
def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")
