import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .role import Role


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
