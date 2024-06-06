from django.contrib import admin
from .models import Quiz, Question, Answer, Statistic, QuizStatistic, Timeer

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Statistic)
admin.site.register(QuizStatistic)
admin.site.register(Timeer)
