from django.urls import path
from .views import PostView

urlpatterns = [
    path("posts", PostView.as_view(), name="post-create"),
    path("posts/<str:post_id>", PostView.as_view(), name="post-update-delete"),
    path("posts/<str:post_id>/history/", PostView.as_view(), name="post-history"),
]
