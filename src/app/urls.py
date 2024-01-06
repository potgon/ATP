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
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from app.dashboard.views import RegisterUserView, login_page, register_page
from app.evaluation_core.views import ListAlgorithmsView, ListAssetsView
from app.trading_data.views import OpenPositionView, ClosePositionView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/algorithms/", ListAlgorithmsView.as_view(), name="list-algorithms"),
    path("api/assets/", ListAssetsView.as_view(), name="list-assets"),
    path("api/trade/open/", OpenPositionView.as_view(), name="open-position"),
    path("api/trade/close/<int:trade_id>/", ClosePositionView.as_view(), name="close-position"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("login-page/", login_page, name="login-page"),
    path("register/", RegisterUserView.as_view({"post": "create"}), name="register"),
    path("register-page/", register_page, name="register-page"),
]
