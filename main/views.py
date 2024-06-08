from pstats import Stats

from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer, Statistic, QuizStatistic, Timer
from .forms import QuizForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.db.models import Q

# Initialize session variables if they do not exist 
def initialize_session_variables(request):
    if "counter" not in request.session:
        request.session["counter"] = 0
    if "counter1" not in request.session:
        request.session["counter1"] = 0


# User login view
def login_page(request):

    page = "login"

    initialize_session_variables(request)

    if request.user.is_authenticated:
        return redirect("home_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home_page")
    context = {"page": page}
    return render(request, "main/login_register.html", context)


# User logout view
def logout_user(request):
    request.session.flush()
    logout(request)
    return redirect("home_page")


# User registration view
def register_page(request):

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.save()
            login(request, user)
            return redirect("home_page")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "main/login_register.html", {"form": form})


# Home page view with quiz search functionality
def home_page(request):

    if Quiz.objects.all().count() > 2:
        reset_quiz_statistics(request)

    q = request.GET.get("q") if request.GET.get("q") != None else ""

    quiz = Quiz.objects.filter(
        Q(quizName__icontains=q) | Q(author__username__icontains=q), public=True
    )

    context = {"quiz": quiz}

    return render(request, "main/home_page.html", context)


# View to create a new quiz
@login_required(login_url="/login")
def create_quiz(request):
    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            if quiz.numberOfQuestions > 0:
                quiz.author = request.user
                quiz.save()
                return redirect("create_questions", quiz_id=quiz.id)

    context = {"form": form}
    return render(request, "main/create_quiz.html", context)


# View to create questions for a quiz
@login_required(login_url="/login")
def create_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuestionForm()
    error_message = ""

    initialize_session_variables(request)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)

            if (
                question.rightAnswer == question.answer1
                or question.rightAnswer == question.answer2
                or question.rightAnswer == question.answer3
                or question.rightAnswer == question.answer4
            ):

                question.quizz = quiz
                question.save()
                request.session["counter"] += 1
                form = QuestionForm()
                if quiz.numberOfQuestions > request.session["counter"]:
                    request.method = "GET"
                else:
                    request.session["counter"] = 0
                    return redirect("home_page")
            else:
                error_message = "Right answer dosen't match with any answers"

    context = {"form": form, "quiz": quiz, "error_message": error_message}
    return render(request, "main/create_questions.html", context)


# View to reset quiz statistics before playing a quiz
def pre_play_check(request, quiz_id):
    reset_quiz_statistics(request)
    return redirect("play_quiz", quiz_id=quiz_id)


# View to play a quiz
@login_required(login_url="/login")
def play_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questionsList = Question.objects.filter(quizz=quiz)

    initialize_session_variables(request)

    if request.session["counter1"] == 0:
        timer = timezone.now()
        tim = Timer.objects.create(time1=timer)

        quizStats = QuizStatistic.objects.create(quiz=quiz, user=request.user)

        request.session["counter1"] = 1

    if request.method == "POST":
        answer = request.POST["answer"]
        if answer:
            a = Answer.objects.create(
                quizQuestion=questionsList[request.session["counter"]].question,
                question=questionsList[request.session["counter"]],
                userAnswer=answer,
                rightAnswer=questionsList[request.session["counter"]].rightAnswer,
                player=request.user,
            )
            update_user_statistics(
                request, questionsList[request.session["counter"]].id, a.id
            )
            request.session["counter"] += 1
            if request.session["counter"] >= len(questionsList):
                request.session["counter"] = 0
                request.session["counter1"] = 0
                tim2 = Timer.objects.all().last()
                timerrr = (timezone.now() - tim2.time1).total_seconds()
                quizStats = QuizStatistic.objects.filter(user=request.user).last()
                quizStats.time = round(timerrr, 2)
                quizStats.save()
                return redirect("after_play_quiz", quiz_id=quiz_id)
            else:
                request.method = "GET"

    context = {"question": questionsList[request.session["counter"]], "quiz": quiz}
    return render(request, "main/play_quiz.html", context)


# Function to update user statistics
def update_user_statistics(request, question_id, answer_id):

    question = get_object_or_404(Question, id=question_id)
    stats = get_object_or_404(Statistic, user=request.user)
    answer = get_object_or_404(Answer, id=answer_id)
    quizStats = QuizStatistic.objects.filter(user=request.user).last()

    if answer.rightAnswer == answer.userAnswer:
        stats.correctAnswers += 1
        quizStats.correctAnswers += 1
    else:
        stats.wrongAnswers += 1
        quizStats.wrongAnswers += 1

    if (
        Question.objects.filter(quizz=question.quizz)[
            len(Question.objects.filter(quizz=question.quizz)) - 1
        ]
        == question
    ):
        stats.quizPlayed += 1
        quizStats.timePlayed = len(
            QuizStatistic.objects.filter(quiz=question.quizz, user=request.user)
        )

    quizStats.save()
    stats.save()


# View to display user statistics
@login_required(login_url="/login")
def user_statistic(request):

    reset_quiz_statistics(request)

    user = User.objects.get(id=request.user.id)

    stats = get_object_or_404(Statistic, user=user)

    quizStats = QuizStatistic.objects.filter(user=user).order_by("-datePlayed")

    context = {"stats": stats, "quizStats": quizStats}

    return render(request, "main/statistics.html", context)


# Function that create user statistics upon user creation
@receiver(post_save, sender=User)
def create_user_statistic(sender, instance, created, **kwargs):
    if created:
        Statistic.objects.create(user=instance)


# View to display quizzes created by the user
@login_required(login_url="/login")
def user_quizzes(request):

    user = User.objects.get(id=request.user.id)
    quizzes = Quiz.objects.filter(author=user)

    context = {"user": user, "quizzes": quizzes}

    return render(request, "main/user_quizzes.html", context)


# Function to create quiz statistics
def create_quiz_statistics(request, quiz_id, time):

    user = User.objects.get(id=request.user.id)
    quiz = Quiz.objects.get(id=quiz_id)
    userStats = Statistic.objects.filter(user=user)
    userStats1 = userStats[len(userStats) - 1]

    quizStats = QuizStatistic.objects.create(
        correctAnswers=userStats1.correctAnswers,
        wrongAnswers=userStats1.wrongAnswers,
        timePlayed=len(userStats),
        time=time,
        quiz=quiz,
        user=user,
    )


# Function to reset quiz statistics, like timer and counters
def reset_quiz_statistics(request):

    quizStatistic = QuizStatistic.objects.all().last()
    if quizStatistic:
        if quizStatistic.time == 0:
            quizStatistic.delete()
            request.session["counter"] = 0
            request.session["counter1"] = 0
            request.session["timer"] = 0


# View to display user statistic of selected quiz before playing it
def pre_play_quiz(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)

    quizStats = QuizStatistic.objects.filter(
        quiz=quiz, timePlayed=1, correctAnswers=quiz.numberOfQuestions
    ).order_by("time")

    context = {"quizStats": quizStats, "q": quiz}

    return render(request, "main/pre_play_quiz.html", context)


def delete_quiz(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    quiz.delete()
    return redirect("user_quizzes")


def toggle_quiz_publicity(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.public:
        quiz.public = False
    else:
        quiz.public = True
    quiz.save()
    return redirect("user_quizzes")


# View to display quiz statistics after quiz had been played
def after_play_quiz(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    numberOfQuestions = quiz.numberOfQuestions

    initialize_session_variables(request)

    answer = Answer.objects.all().order_by("-id")[:numberOfQuestions][::-1]

    time = QuizStatistic.objects.filter(user=request.user).last().time

    context = {"quiz": quiz, "questions": answer, "time": time}

    return render(request, "main/after_play_quiz.html", context)
