# Generated by Django 5.0 on 2023-12-26 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIapp', '0003_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='date',
            field=models.CharField(default='26/12/25', max_length=50),
        ),
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]