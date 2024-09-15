from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
)

from core.utils.helpers import routers
from .views import CurrentUserView, UserLoginView, UserRegisterView

router = routers.OptionalSlashRouter()

app_name = "auth"

urlpatterns = [
    path("auth/register", UserRegisterView.as_view(), name="register"),
    path("auth/login", UserLoginView.as_view(), name="login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="refresh"),
    path("auth/logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/current-user", CurrentUserView.as_view(), name="current-user"),
]
