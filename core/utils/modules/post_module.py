from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.posts.models import Post
from ...v1.posts.repositories import PostRepository
from ...v1.posts.services import PostService
from ...v1.users.repositories import UserRepository


class PostModule(Module):
    @provider
    @singleton
    def provide_post_service(
        self, post_repository: PostRepository, user_repository: UserRepository
    ) -> PostService:
        return PostService(
            post_repository=post_repository,
            user_repository=user_repository,
        )
