# Generated by Django 4.1.7 on 2023-05-14 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_post_post_author_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_author_image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_likes_count',
        ),
    ]
