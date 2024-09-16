import uuid
import os
from django.db import models
from django.conf import settings
from ....utils.helpers.files import generic_image_upload_to


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=False)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=False, blank=True)
    main_image = models.ImageField(
        upload_to="blog-images/",  # Placeholder upload path
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_blog = Blog.objects.get(pk=self.pk)
                if old_blog.main_image and old_blog.main_image != self.main_image:
                    # Remove the old image file
                    if os.path.isfile(old_blog.main_image.path):
                        os.remove(old_blog.main_image.path)
            except Blog.DoesNotExist:
                pass

        if self.main_image:
            new_image_name = generic_image_upload_to(
                self, self.main_image.name, "blog-images/"
            )
            self.main_image.name = new_image_name
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.main_image:
            if os.path.isfile(self.main_image.path):
                os.remove(self.main_image.path)
        super(Blog, self).delete(*args, **kwargs)
