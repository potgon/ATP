from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class RegisterUserView(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []


def login_page(request):
    return render(request, "web_index.html")


def register_page(request):
    return render(request, "web_index.html")


def index_page(request):
    return render(request, "index.html")
