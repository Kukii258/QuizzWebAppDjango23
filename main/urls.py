from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats, name="stats"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.homePage, name="homePage"),
    path("createQuiz/", views.createQuiz, name="createQuiz"),
    path(
        "createQuestions/<int:quiz_id>/", views.createQuestions, name="createQuestions"
    ),
    path("playQuiz/<int:quiz_id>/", views.playQuiz, name="playQuiz"),
    path("prePlayCheck/<int:quiz_id>/", views.prePlayCheck, name="prePlayCheck"),
    path("prePlayQuiz/<int:quiz_id>/", views.prePlayQuiz, name="prePlayQuiz"),
    path("userQuizes/", views.userQuizes, name="userQuizes"),
    path("deleteQuiz/<int:quiz_id>/", views.deleteQuiz, name="deleteQuiz"),
    path(
        "changePublicity/<int:quiz_id>/", views.changePublicity, name="changePublicity"
    ),
    path("afterPlayQuiz/<int:quiz_id>/", views.afterPlayQuiz, name="afterPlayQuiz"),
]
