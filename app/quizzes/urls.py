from django.contrib.auth import views as auth_view
from django.urls import path

from . import views


app_name = 'quizzes'
urlpatterns = [
    path('<str:quiz_number>/', views.QuizView.as_view(), name='quiz'),
]


