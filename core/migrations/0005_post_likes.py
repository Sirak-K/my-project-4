# Generated by Django 4.1.7 on 2023-04-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_id_user_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]