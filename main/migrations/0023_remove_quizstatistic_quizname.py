# Generated by Django 4.2.13 on 2024-05-21 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_quizstatistic_quizname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizstatistic',
            name='quizName',
        ),
    ]