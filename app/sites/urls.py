from django.contrib.auth import views as auth_view
from django.urls import path

from . import views


app_name = 'sites'
urlpatterns = [
    path('', views.LandingPage, name='home'),
    path('ranking/', views.ranking_page, name='ranking'),
]

