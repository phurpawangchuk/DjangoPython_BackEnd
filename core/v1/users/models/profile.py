import uuid

from django.db import models

from .user import User


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    biography = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
