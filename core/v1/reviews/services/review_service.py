from django.core.paginator import Paginator
from injector import inject

from ....utils.exceptions import NotFoundException, ValidationException
from ..repositories import ReviewRepository
from ...posts.repositories import PostRepository
from ...users.repositories import UserRepository

from ..serializers import (
    ReviewCreateRequestSerializer,
    ReviewResponseSerilizer,
    ReviewUpdateRequestSerializer,
)


class ReviewService:
    @inject
    def __init__(
        self,
        review_repository: ReviewRepository,
        post_repository: PostRepository,
        user_repository: UserRepository,
    ):
        self.post_repository = post_repository
        self.review_repository = review_repository
        self.use_repository = user_repository

    def __find_review_by_id(self, review_id):
        try:
            review = self.review_repository.find_by_id(review_id)
            return review
        except Exception:
            raise NotFoundException("Review not found.")

    def get_reviews(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        reviews = self.review_repository.find_all() or []

        paginator = Paginator(reviews, limit)
        page_obj = paginator.get_page(page)

        return (
            ReviewResponseSerilizer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def get_review(self, review_id):
        review = self.__find_review_by_id(review_id)
        return ReviewResponseSerilizer(review).data

    def create_review(self, review_data):
        post_id = review_data["post_id"]
        user_id = review_data["user_id"]

        post = self.post_repository.find_by_id(post_id)
        user = self.use_repository.find_by_id(user_id)

        if not post:
            raise ValidationException(detail={"post": "Post not found."})
        if not user:
            raise ValidationException(detail={"user": "User not found."})

        review_data["post"] = post.id
        review_data["user"] = user.id

        serializer = ReviewCreateRequestSerializer(data=review_data)

        if serializer.is_valid():
            review = serializer.save()
            return ReviewResponseSerilizer(review).data
        raise ValidationException(detail=serializer.errors)

    def update_review(self, review_id, review_data, partial=False):
        review = self.__find_review_by_id(review_id)
        serializer = ReviewUpdateRequestSerializer(data=review_data, partial=partial)

        if serializer.is_valid():
            review = serializer.save()
            return ReviewResponseSerilizer(review).data
        else:
            raise ValidationException(detail=serializer.errors)

    def delete_review(self, review_id):
        review = self.__find_review_by_id(review_id)
        review.delete()
