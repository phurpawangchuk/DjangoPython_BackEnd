from rest_framework import serializers

from ..models import Role


class RoleCreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name", "description"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
        }


class RoleUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name", "description"]


class RoleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description"]
