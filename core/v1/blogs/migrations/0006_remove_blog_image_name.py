# Generated by Django 5.0.8 on 2024-09-15 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_blog_main_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='image_name',
        ),
    ]
