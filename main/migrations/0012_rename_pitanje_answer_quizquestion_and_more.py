# Generated by Django 4.2.13 on 2024-05-21 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_answer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="answer",
            old_name="pitanje",
            new_name="quizQuestion",
        ),
        migrations.RenameField(
            model_name="answer",
            old_name="tocanOdgovor",
            new_name="rightAnswer",
        ),
        migrations.RenameField(
            model_name="answer",
            old_name="odgovorKorisnika",
            new_name="userAnswer",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="odgovor1",
            new_name="answer1",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="odgovor2",
            new_name="answer2",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="odgovor3",
            new_name="answer3",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="odgovor4",
            new_name="answer4",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="pitanje",
            new_name="question",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="tocanOdgovor",
            new_name="rightAnswer",
        ),
        migrations.RenameField(
            model_name="quiz",
            old_name="brojPitanja",
            new_name="numberOfQuestions",
        ),
        migrations.RenameField(
            model_name="quiz",
            old_name="imeQuiza",
            new_name="quizName",
        ),
    ]
