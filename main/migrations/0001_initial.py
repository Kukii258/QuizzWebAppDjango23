# Generated by Django 4.2.13 on 2024-05-16 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("imeQuiza", models.CharField(max_length=100)),
                ("brojPitanja", models.IntegerField(max_length=11)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pitanje1", models.CharField(max_length=100)),
                ("odgovor1", models.CharField(max_length=100)),
                ("odgovor2", models.CharField(max_length=100)),
                ("odgovor3", models.CharField(max_length=100)),
                ("odgovor4", models.CharField(max_length=100)),
                ("tocanOdgovor", models.CharField(max_length=100)),
                ("odgovorKorisnika", models.CharField(max_length=100)),
                (
                    "quizz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.quiz"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
