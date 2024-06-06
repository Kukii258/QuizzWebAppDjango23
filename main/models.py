from django.utils import timezone

from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Statistic(models.Model):
    quizPlayed = models.IntegerField(default=0)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Quiz(models.Model):
    quizName = models.CharField(max_length=100)
    numberOfQuestions = models.IntegerField(null=True, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.quizName


class Timeer(models.Model):
    time1 = models.DateTimeField(default=timezone.now)
    time2 = models.DateTimeField(default=timezone.now)
    finalTime = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    question = models.CharField(max_length=100)
    answer1 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)
    answer3 = models.CharField(max_length=100)
    answer4 = models.CharField(max_length=100)
    rightAnswer = models.CharField(max_length=100)
    quizz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    userAnswer = models.CharField(max_length=100)
    quizQuestion = models.CharField(max_length=100)
    rightAnswer = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.userAnswer


class QuizStatistic(models.Model):
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    datePlayed = models.DateTimeField(auto_now_add=True)
    time = models.FloatField(default=0)
    timePlayed = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
