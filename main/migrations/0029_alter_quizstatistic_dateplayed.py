# Generated by Django 4.2.13 on 2024-05-21 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_quizstatistic_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizstatistic",
            name="datePlayed",
            field=models.DateField(default="21:23 21.05.2024"),
        ),
    ]
