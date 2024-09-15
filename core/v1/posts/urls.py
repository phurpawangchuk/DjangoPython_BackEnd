from django.urls import path
from .views import PostView

from core.utils.helpers import routers

router = routers.OptionalSlashRouter()

app_name = "core.v1.posts"

urlpatterns = [
    path("posts", PostView.as_view(), name="post-create"),
    path("posts/<str:post_id>", PostView.as_view(), name="post-update-delete"),
    path("posts/<str:post_id>/history/", PostView.as_view(), name="post-history"),
]
