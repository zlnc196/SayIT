# Generated by Django 5.0 on 2024-02-17 00:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIapp', '0015_posts_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followedUsers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default=[], max_length=100), default=[], size=None),
            preserve_default=False,
        ),
    ]
