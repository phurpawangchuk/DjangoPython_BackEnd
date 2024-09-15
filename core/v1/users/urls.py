from django.urls import path

from core.utils.helpers import routers

from .views import ProfileView, RoleView, UserView

router = routers.OptionalSlashRouter()

app_name = "users"

urlpatterns = [
    # UserView
    path("users", UserView.as_view(), name="user-list-create"),
    path("users/<str:user_id>", UserView.as_view(), name="user-detail-update-delete"),
    # ProfileView
    path(
        "users/<str:user_id>/profile",
        ProfileView.as_view(),
        name="profile-detail-update-delete",
    ),
    # RoleView
    path("roles", RoleView.as_view(), name="role-list-create"),
    path("roles/<str:role_id>", RoleView.as_view(), name="role-detail-update-delete"),
]
