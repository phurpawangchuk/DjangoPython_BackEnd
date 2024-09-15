from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.users.models import User
from ...v1.users.repositories import RoleRepository, UserRepository
from ...v1.users.services import UserService


class UserModule(Module):
    @provider
    @singleton
    def provide_user_model(self) -> Type[User]:
        return apps.get_model("users", "User")

    @provider
    @singleton
    def provide_user_repository(self, user_model: Type[User]) -> UserRepository:
        return UserRepository(model=user_model)

    @provider
    @singleton
    def provide_user_service(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ) -> UserService:
        return UserService(
            user_repository=user_repository, role_repository=role_repository
        )
