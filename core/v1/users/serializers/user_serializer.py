from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Role

User = get_user_model()


class UserCreateRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "role"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.role = validated_data["role"]
        user.save()
        return user


class UserUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserResponseSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        ]


class UserResponseMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
