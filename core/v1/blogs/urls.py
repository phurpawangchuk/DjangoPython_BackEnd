from django.urls import path
from .views import BlogView

urlpatterns = [
    path("blogs", BlogView.as_view(), name="blog-create"),
    path("blogs/<str:blog_id>", BlogView.as_view(), name="blog-update-delete"),
]
