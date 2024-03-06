from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.trading_data.broker import Broker
from app.trading_data.tasks import manage_request, schedule_algo

from .models import Algorithm, Asset
from .serializers import AlgorithmSerializer, AssetSerializer, RunAlgorithmSerializer


class RunAlgorithmView(GenericViewSet):
    @method_decorator(ensure_csrf_cookie)
    @action(detail=True, methods=["get", "post"])
    def run(self, request, *args, **kwargs):
        if request.method == "POST":
            serializer = RunAlgorithmSerializer(data=request.data)
            if serializer.is_valid():
                manage_request(
                    serializer.validated_data.get("algo_name"),
                    Asset.objects.get(
                        name=serializer.validated_data.get("name".upper())
                    ).ticker,
                )
                schedule_algo.delay(
                    serializer.validated_data.get("algo_name"), Broker()
                )
                return Response(
                    {
                        "message": f"{serializer.validated_data.get('algo_name')} started successfully"
                    }
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, "run_algorithm.html")


class ListAlgorithmsView(GenericViewSet, ListModelMixin):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

    def list(self, request, *args, **kwargs):
        return super(ListAlgorithmsView, self).list(request, *args, **kwargs)


class ListAssetsView(GenericViewSet, ListModelMixin):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def list(self, request, *args, **kwargs):
        return super(ListAssetsView, self).list(request, *args, **kwargs)
