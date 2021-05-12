from django.contrib.auth import views as auth_view
from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', auth_view.LogoutView.as_view(), name='signout'),
]
