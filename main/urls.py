from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.user_statistic, name="stats"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.home_page, name="home_page"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path(
        "create-questions/<int:quiz_id>/",
        views.create_questions,
        name="create_questions",
    ),
    path("play-quiz/<int:quiz_id>/", views.play_quiz, name="play_quiz"),
    path("pre-play-check/<int:quiz_id>/", views.pre_play_check, name="pre_play_check"),
    path("pre-play-quiz/<int:quiz_id>/", views.pre_play_quiz, name="pre_play_quiz"),
    path("user-quizzes/", views.user_quizzes, name="user_quizzes"),
    path("delete-quiz/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
    path(
        "change-publicity/<int:quiz_id>/",
        views.toggle_quiz_publicity,
        name="change_publicity",
    ),
    path(
        "after-play-quiz/<int:quiz_id>/", views.after_play_quiz, name="after_play_quiz"
    ),
]
