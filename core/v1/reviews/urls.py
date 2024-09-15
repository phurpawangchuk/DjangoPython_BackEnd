from django.urls import path
from .views import ReviewView

from core.utils.helpers import routers

router = routers.OptionalSlashRouter()

app_name = "core.v1.reviews"

urlpatterns = [
    path("reviews", ReviewView.as_view(), name="review-create"),
    path("reviews/<str:review_id>", ReviewView.as_view(), name="review-update-delete"),
]
