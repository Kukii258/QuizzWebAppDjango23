from pstats import Stats

from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer, Statistic, QuizStatistic,Timeer
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
from django.shortcuts import render


def initialize_session_variables(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    if 'counter1' not in request.session:
        request.session['counter1'] = 0




def loginPage(request):

    page = 'login'

    initialize_session_variables(request)

    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            messages.error(request, 'Usermae or password not exist')
    context = {'page':page}
    return render(request, 'main/login_register.html', context)
def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('homePage')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homePage')
        else:
            messages.error(request, 'Error.')


    return render(request, 'main/login_register.html', {'form':form})

def homePage(request):

    if Quiz.objects.all().count() > 2:
        quizNull(request)


    q = request.GET.get('q') if request.GET.get('q') != None else ''

    quiz = Quiz.objects.filter(
        Q(quizName__icontains=q)|
        Q(author__username__icontains=q),
        public = True
    )

    context = {'quiz': quiz}

    return render(request, 'main/homePage.html', context)

@login_required(login_url='/login')
def createQuiz(request):
    form = QuizForm()

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('createQuestions', quiz_id=quiz.id)

    context = {'form': form}
    return render(request, '/main/createQuiz.html', context)
@login_required(login_url='/login')
def createQuestions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuestionForm()
    error_message =""

    initialize_session_variables(request)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)

            if (question.rightAnswer == question.answer1 or question.rightAnswer == question.answer2 or question.rightAnswer == question.answer3 or question.rightAnswer == question.answer4):

                question.quizz = quiz
                question.save()
                request.session['counter']+=1
                form = QuestionForm()
                if (quiz.numberOfQuestions > request.session['counter']):
                    request.method = 'GET'
                else:
                    request.session['counter'] = 0
                    return redirect('homePage')
            else:
                error_message = "Tocan odgovor se ne podudara s niti jednim odgovorom"


    context = {'form': form, 'quiz': quiz,'error_message': error_message}
    return render(request, 'main/createQuestions.html', context)


def prePlayCheck(request, quiz_id):
    quizNull(request)
    return redirect('playQuiz', quiz_id=quiz_id)

@login_required(login_url='/login')
def playQuiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questionsList = Question.objects.filter(quizz=quiz)

    initialize_session_variables(request)

    if request.session['counter1']  == 0:
        timer = timezone.now()
        tim = Timeer.objects.create(time1 = timer)

        quizStats = QuizStatistic.objects.create(
             quiz=quiz, user=request.user
        )

        request.session['counter1'] = 1

    if request.method == 'POST':
        answer = request.POST['answer']
        if answer :
            a = Answer.objects.create(quizQuestion=questionsList[request.session['counter']].question, question=questionsList[request.session['counter']],
                                      userAnswer=answer, rightAnswer=questionsList[request.session['counter']].rightAnswer,
                                      player = request.user)
            userStatistics(request, questionsList[request.session['counter']].id, a.id)
            request.session['counter'] += 1
            if request.session['counter'] >= len(questionsList):
                request.session['counter'] = 0
                request.session['counter1'] = 0
                tim2 = Timeer.objects.all().last()
                timerrr = (timezone.now() - tim2.time1).total_seconds()
                quizStats = QuizStatistic.objects.filter(user = request.user).last()
                quizStats.time = round(timerrr,2)
                quizStats.save()
                return redirect('afterPlayQuiz', quiz_id=quiz_id)
            else:
                request.method = 'GET'

    context = {'question': questionsList[request.session['counter']], 'quiz': quiz}
    return render(request, 'main/playQuiz.html', context)

def userStatistics(request, question_id, answer_id):

    question = get_object_or_404(Question, id=question_id)
    stats = get_object_or_404(Statistic, user = request.user)
    answer = get_object_or_404(Answer, id = answer_id)
    quizStats = QuizStatistic.objects.filter(user = request.user).last()

    if answer.rightAnswer == answer.userAnswer:
        stats.correctAnswers += 1
        quizStats.correctAnswers += 1
    else:
        stats.wrongAnswers += 1
        quizStats.wrongAnswers += 1

    if Question.objects.filter(quizz=question.quizz)[len(Question.objects.filter(quizz=question.quizz))-1] == question:
        stats.quizPlayed += 1
        quizStats.timePlayed = len(QuizStatistic.objects.filter(quiz = question.quizz,user = request.user))

    quizStats.save()
    stats.save()

@login_required(login_url='/login')
def stats(request):

    quizNull(request)

    user = User.objects.get(id=request.user.id)

    stats = get_object_or_404(Statistic, user=user)

    quizStats = QuizStatistic.objects.filter(user = user).order_by('-datePlayed')

    context = {'stats':stats,'quizStats':quizStats}

    return render(request, 'main/stats.html', context)


@receiver(post_save, sender=User)
def create_user_statistic(sender, instance, created, **kwargs):
    if created:
        Statistic.objects.create(user=instance)


@login_required(login_url='/login')
def userQuizes(request):

    user = User.objects.get(id=request.user.id)
    quizzes = Quiz.objects.filter(author=user)

    context = {'user':user, 'quizzes':quizzes}

    return render(request, 'main/userQuizes.html', context)

def quizStats(request,quiz_id,time):

    user = User.objects.get(id=request.user.id)
    quiz = Quiz.objects.get(id = quiz_id)
    userStats = Statistic.objects.filter(user=user)
    userStats1 = userStats[len(userStats)-1]

    quizStats = QuizStatistic.objects.create(
        correctAnswers=userStats1.correctAnswers, wrongAnswers=userStats1.wrongAnswers,
        timePlayed=len(userStats),time=time,quiz=quiz,user=user
    )

def quizNull(request):


    quizStatistic = QuizStatistic.objects.all().last()
    if quizStatistic:
        if quizStatistic.time == 0:
            quizStatistic.delete()
            request.session['counter'] = 0
            request.session['counter1'] = 0
            request.session['timer'] = 0

def prePlayQuiz(request,quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)

    quizStats = QuizStatistic.objects.filter(quiz = quiz,timePlayed=1).order_by('time')

    context = {'quizStats':quizStats,'q':quiz}

    return render(request, 'main/prePlayQuiz.html', context)

def deleteQuiz(request,quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    quiz.delete()
    return redirect('userQuizes')

def changePublicity(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.public:
        quiz.public = False
    else:
        quiz.public = True
    quiz.save()
    return redirect('userQuizes')

def afterPlayQuiz(request,quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    numberOfQuestions = quiz.numberOfQuestions

    initialize_session_variables(request)

    answer = Answer.objects.all().order_by('-id')[:numberOfQuestions][::-1]

    time = QuizStatistic.objects.filter(user=request.user).last().time

    context = {'quiz':quiz,'questions':answer,'time':time}

    return render(request, 'main/afterPlayQuiz.html', context)
