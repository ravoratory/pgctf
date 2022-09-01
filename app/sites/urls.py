from django.urls import path

from . import views
from quizzes.views import quiz_list_view


app_name = 'sites'
urlpatterns = [
    path('', quiz_list_view, name='home'),
    path('ranking/', views.ranking_page, name='ranking'),
    path('ranking-chart/', views.ranking_chart, name='ranking_chart'),
]
