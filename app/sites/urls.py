from django.contrib.auth import views as auth_view
from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('home/', views.LandingPage, name='home'),
]

