import os
from django.utils.text import slugify
from datetime import datetime


def generic_image_upload_to(instance, filename, folder):
    _, file_extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}{file_extension}"
    return f"{new_filename}"


#     return f"{folder}/{slug}-{new_filename}"
