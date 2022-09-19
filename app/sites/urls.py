from django.urls import path

from quizzes.views import QuizListView

from . import views

app_name = "sites"
urlpatterns = [
    # path('', quiz_list_view, name='home'),
    path("", QuizListView.as_view(), name="home"),
    path("ranking/", views.RankingView.as_view(), name="ranking"),
    path("ranking-chart/", views.ranking_chart, name="ranking_chart"),
]
