from django.urls import path

from . import views


app_name = 'problems'
urlpatterns = [
    path('only_invalid_ip', views.only_invalid_ip, name='only_invalid_ip'),
]

