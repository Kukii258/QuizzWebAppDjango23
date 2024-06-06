# Generated by Django 4.2.13 on 2024-05-20 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_alter_quiz_brojpitanja"),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
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
                ("odgovorKorisnika", models.CharField(max_length=100)),
                ("pitanje", models.CharField(max_length=100)),
                ("tocanOdgovor", models.CharField(max_length=100)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.question"
                    ),
                ),
            ],
        ),
    ]
