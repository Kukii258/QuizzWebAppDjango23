# Generated by Django 4.2.13 on 2024-05-20 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_quiz_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 5, 20, 7, 30, 3, 151348, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
