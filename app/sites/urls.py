from django.urls import path

from . import views
from quizzes.views import QuizListView


app_name = 'sites'
urlpatterns = [
    # path('', quiz_list_view, name='home'),
    path('', QuizListView.as_view(), name='home'),
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('ranking-chart/', views.ranking_chart, name='ranking_chart'),
]
