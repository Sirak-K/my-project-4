# Generated by Django 4.1.7 on 2023-05-11 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_post_comment_comment_for_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_for_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post'),
        ),
    ]
