import uuid
from django.db import models
from ....v1.posts.models.post import Post
from ....v1.users.models.user import User


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comments = models.CharField(max_length=255)
    rating = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
