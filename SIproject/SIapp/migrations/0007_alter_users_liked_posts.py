# Generated by Django 5.0 on 2023-12-29 20:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIapp', '0006_users_liked_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='liked_posts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default=[], max_length=100), default=[], size=None),
            preserve_default=False,
        ),
    ]