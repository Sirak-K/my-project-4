# Generated by Django 4.1.6 on 2023-06-06 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_remove_friendship_friend_request_friendship_receiver_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='status',
        ),
        migrations.AddField(
            model_name='friendship',
            name='friendship_receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_friendships', to='core.friendrequest'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='friendship_sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiated_friendships', to='core.friendrequest'),
        ),
    ]