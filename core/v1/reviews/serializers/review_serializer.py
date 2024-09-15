from rest_framework import serializers
from django.db import transaction
from ..models import Review
from ....v1.posts.models import Post
from ....v1.users.models import User

from ....v1.posts.serializers import (
    PostResponseSerializer,
    PostResponseWithoutUserSerializer,
)
from ....v1.users.serializers import UserResponseMinimalSerializer


class ReviewCreateRequestSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Review
        fields = ["id", "comments", "rating", "post", "user"]

    def create(self, validated_data):
        with transaction.atomic():
            post = validated_data.pop("post", None)
            user = validated_data.pop("user", None)
            review = Review.objects.create(post=post, user=user, **validated_data)
            return review


class ReviewUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["comments", "rating"]


class ReviewResponseSerilizer(serializers.ModelSerializer):
    post = PostResponseWithoutUserSerializer(read_only=True)
    user = UserResponseMinimalSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "comments", "rating", "post", "user"]
