# Generated by Django 5.0 on 2024-01-27 17:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIapp', '0014_customuser_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='replies',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default=[], max_length=100), default=[], size=None),
            preserve_default=False,
        ),
    ]