# Generated by Django 4.1.7 on 2023-05-31 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_remove_friendship_status_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='friendship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friendship_request', to='core.friendship'),
        ),
    ]
