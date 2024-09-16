from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.blogs.models import Blog
from ...v1.blogs.repositories import BlogRepository
from ...v1.blogs.services import BlogService
from ...v1.users.repositories import UserRepository


class BlogModule(Module):
    @provider
    @singleton
    def provide_Blog_service(
        self,
        blog_repository: BlogRepository,
        user_repository: UserRepository,
    ) -> BlogService:
        return BlogService(
            blog_repository=blog_repository,
            user_repository=user_repository,
        )
