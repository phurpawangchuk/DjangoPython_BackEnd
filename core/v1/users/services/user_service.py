from django.core.paginator import Paginator
from injector import inject

from ....utils.exceptions import NotFoundException, ValidationException
from ..repositories import RoleRepository, UserRepository
from ..serializers import (
    UserCreateRequestSerializer,
    UserResponseSerializer,
    UserUpdateRequestSerializer,
)


class UserService:
    @inject
    def __init__(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def get_users(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        users = self.user_repository.find_all() or []

        paginator = Paginator(users, limit)
        page_obj = paginator.get_page(page)

        return (
            UserResponseSerializer(page_obj, many=True).data,
            paginator.count,
            paginator.num_pages,
            page_obj.number,
        )

    def __find_user_by_id(self, user_id):
        try:
            user = self.user_repository.find_by_id(user_id)
            return user
        except Exception:
            raise NotFoundException("User not found.")

    def get_user(self, user_id):
        user = self.__find_user_by_id(user_id)
        return UserResponseSerializer(user).data

    def create_user(self, user_data):
        role = user_data.get("role")
        if not self.role_repository.exists(role):
            raise ValidationException({"role": ["Invalid role ID provided."]})

        serializer = UserCreateRequestSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            return UserResponseSerializer(user).data
        else:
            raise ValidationException(detail=serializer.errors)

    def update_user(self, user_id, user_data, partial=False):
        user = self.__find_user_by_id(user_id)
        serializer = UserUpdateRequestSerializer(user, data=user_data, partial=partial)

        if serializer.is_valid():
            user = serializer.save()
            return UserResponseSerializer(user).data
        else:
            raise ValidationException(detail=serializer.errors)

    def delete_user(self, user_id):
        user = self.__find_user_by_id(user_id)
        user.delete()
