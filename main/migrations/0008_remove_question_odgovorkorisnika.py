# Generated by Django 4.2.13 on 2024-05-20 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_question_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='odgovorKorisnika',
        ),
    ]
