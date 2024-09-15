from django.core.paginator import Paginator
from injector import inject

from ....utils.exceptions import NotFoundException, ValidationException
from ..repositories import PostRepository
from ...users.repositories import UserRepository
from ..serializers import (
    PostCreateRequestSerializer,
    PostResponseSerializer,
    PostUpdateRequestSerializer,
    PostAuditHistorySerializer,
)


class PostService:
    @inject
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
    ):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def __find_post_by_id(self, post_id):
        try:
            post = self.post_repository.find_by_id(post_id)
            return post
        except Exception:
            raise NotFoundException("Post not found.")

    def get_posts(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        posts = self.post_repository.find_all() or []

        paginator = Paginator(posts, limit)
        page_obj = paginator.get_page(page)

        return (
            PostResponseSerializer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def get_post_history(self, post_id, request):

        post = self.__find_post_by_id(post_id)
        history_records = post.history.all()

        if not history_records:
            raise NotFoundException("No history found for the post.")

        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)

        paginator = Paginator(history_records, limit)
        page_obj = paginator.get_page(page)

        return (
            PostAuditHistorySerializer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def get_post(self, post_id):
        post = self.__find_post_by_id(post_id)
        return PostResponseSerializer(post).data

    def create_post(self, post_data):
        user_id = post_data["user_id"]
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise ValidationException(detail={"user": "User not found."})

        post_data["user"] = user.id

        serializer = PostCreateRequestSerializer(data=post_data)

        if serializer.is_valid():
            post = serializer.save()
            return PostResponseSerializer(post).data
        raise ValidationException(detail=serializer.errors)

    def update_post(self, post_id, post_data, partial=False):
        post = self.__find_post_by_id(post_id)

        serializer = PostUpdateRequestSerializer(post, data=post_data, partial=partial)

        if serializer.is_valid():
            post = serializer.save()
            return PostResponseSerializer(post).data
        else:
            raise ValidationException(detail=serializer.errors)

    def delete_post(self, post_id):
        post = self.__find_post_by_id(post_id)
        post.delete()
