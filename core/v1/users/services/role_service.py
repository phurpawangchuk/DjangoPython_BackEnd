from django.core.paginator import Paginator
from injector import inject

from ....utils.exceptions import NotFoundException, ValidationException
from ..repositories import RoleRepository
from ..serializers import (
    RoleCreateRequestSerializer,
    RoleResponseSerializer,
    RoleUpdateRequestSerializer,
)


class RoleService:
    @inject
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def get_roles(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        roles = self.role_repository.find_all() or []

        paginator = Paginator(roles, limit)
        page_obj = paginator.get_page(page)

        return (
            RoleResponseSerializer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def __find_role_by_id(self, role_id):
        try:
            role = self.role_repository.find_by_id(role_id)
            return role
        except Exception:
            raise NotFoundException("Role not found.")

    def get_role(self, role_id):
        role = self.__find_role_by_id(role_id)
        return RoleResponseSerializer(role).data

    def create_role(self, role_data):
        serializer = RoleCreateRequestSerializer(data=role_data)

        if serializer.is_valid():
            role = serializer.save()
            return RoleResponseSerializer(role).data
        raise ValidationException(detail=serializer.errors)

    def update_role(self, role_id, role_data, partial=False):
        role = self.__find_role_by_id(role_id)
        serializer = RoleUpdateRequestSerializer(role, data=role_data, partial=partial)

        if serializer.is_valid():
            role = serializer.save()
            return RoleResponseSerializer(role).data
        else:
            raise ValidationException(detail=serializer.errors)

    def delete_role(self, role_id):
        role = self.__find_role_by_id(role_id)
        role.delete()
