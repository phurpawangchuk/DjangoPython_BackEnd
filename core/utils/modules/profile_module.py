from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.users.models import Profile
from ...v1.users.repositories import ProfileRepository, UserRepository
from ...v1.users.services import ProfileService


class ProfileModule(Module):
    @provider
    @singleton
    def provide_profile_model(self) -> Type[Profile]:
        return apps.get_model("users", "Profile")

    @provider
    @singleton
    def provide_profile_repository(
        self, role_model: Type[Profile]
    ) -> ProfileRepository:
        return ProfileRepository(model=role_model)

    @provider
    @singleton
    def provide_role_service(
        self, profile_repository: ProfileRepository, user_repository: UserRepository
    ) -> ProfileService:
        return ProfileService(
            profile_repository=profile_repository, user_repository=user_repository
        )
