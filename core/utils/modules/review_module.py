from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.reviews.models import Review
from ...v1.reviews.repositories import ReviewRepository
from ...v1.reviews.services import ReviewService
from ...v1.users.repositories import UserRepository
from ...v1.posts.repositories import PostRepository


class ReviewModule(Module):
    @provider
    @singleton
    def provide_review_model(self) -> Type[Review]:
        return apps.get_model("reviews", "Review")

    @provider
    @singleton
    def provide_review_repository(self, review_model: Type[Review]) -> ReviewRepository:
        return ReviewRepository(model=review_model)

    @provider
    @singleton
    def provide_review_service(
        self,
        review_repository: ReviewRepository,
        post_repository: PostRepository,
        user_repository: UserRepository,
    ) -> ReviewService:
        return ReviewService(
            review_repository=review_repository,
            post_repository=post_repository,
            user_repository=user_repository,
        )
