from typing import Type

from django.apps import apps
from injector import Module, provider, singleton

from ...v1.users.models import Role
from ...v1.users.repositories import RoleRepository
from ...v1.users.services import RoleService


class RoleModule(Module):
    @provider
    @singleton
    def provide_role_model(self) -> Type[Role]:
        return apps.get_model("users", "Role")

    @provider
    @singleton
    def provide_role_repository(self, role_model: Type[Role]) -> RoleRepository:
        return RoleRepository(model=role_model)

    @provider
    @singleton
    def provide_role_service(self, role_repository: RoleRepository) -> RoleService:
        return RoleService(role_repository=role_repository)
