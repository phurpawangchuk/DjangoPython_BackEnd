from rest_framework import serializers

from ...users.serializers.user_serializer import UserResponseSerializer
from ..models import Blog
from ...users.models import User


class BlogCreateRequestSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "author")
        extra_kwargs = {"title": {"required": True}, "content": {"required": True}}


class BlogUpdateRequestSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Blog
        fields = ["title", "content", "main_image", "author"]


class BlogResponseSerializer(serializers.ModelSerializer):
    author = UserResponseSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"
