"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

from app.dashboard.views import RegisterUserView, index_page, login_page, register_page
from app.evaluation_core.views import (
    ListAlgorithmsView,
    ListAssetsView,
    RunAlgorithmView,
)
from app.trading_data.views import ClosePositionViewSet

router = DefaultRouter()
router.register(r"algorithms", ListAlgorithmsView, basename="algorithms")
router.register(r"assets", ListAssetsView, basename="assets")
router.register(r"run-algo", RunAlgorithmView, basename="run-algo")
router.register(
    r"trade/close/<int:trade-id>", ClosePositionViewSet, basename="close-position"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_page, name="main-page"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("login-page/", login_page, name="login-page"),
    path("register/",
         RegisterUserView.as_view({"post": "create"}), name="register"),
    path("register-page/", register_page, name="register-page"),
    path(
        "run-algo-page/",
        RunAlgorithmView.as_view({"get": "run", "post": "run"}),
        name="run-algorithm",
    ),
    path("api/", include(router.urls)),
]
