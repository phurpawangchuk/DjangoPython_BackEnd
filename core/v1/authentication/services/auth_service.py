from django.contrib.auth import authenticate
from django.utils import timezone
from injector import inject
from rest_framework_simplejwt.tokens import RefreshToken

from ....utils.exceptions import ValidationException
from ...users.repositories import UserRepository
from ...users.serializers import UserResponseSerializer
from ...users.services import UserService
from ..seralizers import (
    TokenSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)


class AuthService:
    @inject
    def __init__(self, user_repository: UserRepository, user_service: UserService):
        self.user_repository = user_repository
        self.user_service = user_service

    def register_user(self, user_data):
        serializer = UserRegistrationSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            return UserResponseSerializer(user).data
        else:
            raise ValidationException(detail=serializer.errors)

    def login_user(self, credentials):
        serializer = UserLoginSerializer(data=credentials)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )

            if user:
                user.last_login = timezone.now()
                user.save(update_fields=["last_login"])
                refresh = RefreshToken.for_user(user)

                return TokenSerializer(
                    {"refresh": str(refresh), "access": str(refresh.access_token)}
                ).data
            else:
                raise ValidationException(
                    detail={"non_field_errors": ["Invalid username or password."]}
                )
        else:
            raise ValidationException(detail=serializer.errors)
