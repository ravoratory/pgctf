from django.urls import path

from . import views


app_name = "quizzes"
urlpatterns = [
    path("<str:number>/", views.QuizView.as_view(), name="quiz"),
]
