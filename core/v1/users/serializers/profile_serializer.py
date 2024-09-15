from django.db import transaction
from rest_framework import serializers

from ..models import Profile, User
from .user_serializer import UserResponseSerializer


class ProfileCreateRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Profile
        fields = ["biography", "birthday", "user"]
        extra_kwargs = {
            "biography": {"required": True},
            "birthday": {"required": True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            user = validated_data.pop("user", None)
            profile = Profile.objects.create(user=user, **validated_data)
            return profile


class ProfileUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["biography", "birthday"]


class ProfileResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "biography",
            "birthday",
        ]
