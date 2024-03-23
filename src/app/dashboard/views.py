from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from app.dashboard.models import User
from .serializers import UserSerializer
from app.utils.logger import make_log


class RegisterUserView(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        make_log("USER", 20, "user.log", f"request data : {request.data}")
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


def login_page(request):
    return render(request, "web_index.html")


def register_page(request):
    return render(request, "web_index.html")


def index_page(request):
    return render(request, "index.html")
