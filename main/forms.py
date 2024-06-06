from django.forms import ModelForm
from .models import Quiz, Question, Answer


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"
        exclude = ["author"]


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ["quizz"]


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ["quizz", "player"]
