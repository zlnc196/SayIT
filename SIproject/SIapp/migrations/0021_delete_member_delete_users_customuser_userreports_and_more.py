# Generated by Django 5.0 on 2024-02-20 14:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIapp', '0020_delete_users_customuser_userreports_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Member',
        ),
    ]
