# Generated by Django 4.1.6 on 2023-05-17 10:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0024_remove_friendlist_user1_remove_friendlist_user2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_title',
            field=models.CharField(max_length=50),
        ),
    ]
