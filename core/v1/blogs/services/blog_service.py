from django.core.paginator import Paginator

from core.utils.exceptions.validation import ValidationException
from core.v1.blogs.serializers.blog_serializer import BlogCreateRequestSerializer
from ..repositories import BlogRepository
from ...users.repositories import UserRepository
from ..serializers import (
    BlogResponseSerializer,
    BlogUpdateRequestSerializer,
)

from injector import inject


class BlogService:
    @inject
    def __init__(
        self,
        blog_repository: BlogRepository,
        user_repository: UserRepository,
    ):
        self.blog_repository = blog_repository
        self.user_repository = user_repository

    def __find_blog_by_id(self, blog_id):
        try:
            blog = self.blog_repository.find_by_id(blog_id)
            return blog
        except Exception:
            raise ValidationException("Blog not found.")

    def get_blogs(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        blogs = self.blog_repository.find_all() or []

        paginator = Paginator(blogs, limit)
        page_obj = paginator.get_page(page)

        return (
            BlogResponseSerializer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def get_blog(self, blog_id):
        blog = self.__find_blog_by_id(blog_id)
        return BlogResponseSerializer(blog).data

    def create_blog(self, blog_data):
        user_id = blog_data.get("author")
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise ValidationException("Author not found.")

        blog_data["author"] = user.id

        serializer = BlogCreateRequestSerializer(data=blog_data)

        if serializer.is_valid():
            blog = serializer.save()
            return BlogResponseSerializer(blog).data
        raise ValidationException(detail=serializer.errors)

    def update_blog(self, blog_id, blog_data, partial=False):
        blog = self.__find_blog_by_id(blog_id)
        serializer = BlogUpdateRequestSerializer(blog, data=blog_data, partial=partial)

        if serializer.is_valid():
            blog = serializer.save()
            return BlogResponseSerializer(blog).data
        raise ValidationException(detail=serializer.errors)

    def delete_blog(self, blog_id):
        blog = self.__find_blog_by_id(blog_id)
        blog.delete()
