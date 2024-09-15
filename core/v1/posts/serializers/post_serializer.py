from rest_framework import serializers
from django.db import transaction
from ..models import Post
from ...users.models import User
from ...users.serializers import UserResponseSerializer


class PostCreateRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Post
        fields = ["id", "title", "description", "user"]

    def create(self, validated_data):
        with transaction.atomic():
            user = validated_data.pop("user", None)
            post = Post.objects.create(user=user, **validated_data)
            return post


class PostUpdateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["title", "description", "user"]


class PostResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "description", "user"]


class PostResponseWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "description"]


class PostAuditHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()
    change_date = serializers.DateTimeField(source="history_date")

    class Meta:
        model = Post.history.model
        fields = ["id", "title", "description", "changed_by", "change_date"]

    def get_changed_by(self, obj):
        if obj.history_user:
            return obj.history_user.username
        return "Unknown"
