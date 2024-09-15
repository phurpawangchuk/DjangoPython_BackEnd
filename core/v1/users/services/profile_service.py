from injector import inject

from ....utils.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from ..repositories import ProfileRepository, UserRepository
from ..serializers import (
    ProfileCreateRequestSerializer,
    ProfileResponseSerializer,
    ProfileUpdateRequestSerializer,
)


class ProfileService:
    @inject
    def __init__(
        self, profile_repository: ProfileRepository, user_repository: UserRepository
    ):
        self.profile_repository = profile_repository
        self.user_repository = user_repository

    def __find_profile_by_user(self, user_id):
        try:
            profile = self.profile_repository.find_profile_by_user(user_id)
            return profile
        except Exception:
            raise NotFoundException("User profile not found.")

    def get_profile(self, user_id):
        profile = self.__find_profile_by_user(user_id)
        return ProfileResponseSerializer(profile).data

    def create_profile(self, user_id, profile_data):
        user = self.user_repository.find_by_id(user_id)
        profile = self.__find_profile_by_user(user_id)

        if not user:
            raise ValidationException({"user": ["Invalid user ID provided."]})

        if profile is not None:
            raise AlreadyExistsException("Profile already exists.")

        profile_data["user"] = user.id
        serializer = ProfileCreateRequestSerializer(data=profile_data)

        if serializer.is_valid():
            profile = serializer.save()
            return ProfileResponseSerializer(profile).data
        else:
            raise ValidationException(detail=serializer.errors)

    def update_profile(self, user_id, profile_data, partial=False):
        profile = self.__find_profile_by_user(user_id)
        serializer = ProfileUpdateRequestSerializer(
            profile, data=profile_data, partial=partial
        )

        if serializer.is_valid():
            profile = serializer.save()
            return ProfileResponseSerializer(profile).data
        else:
            raise ValidationException(detail=serializer.errors)
