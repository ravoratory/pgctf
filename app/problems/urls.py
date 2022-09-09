from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("only_limited_host", views.only_limited_host, name="only_limited_host"),
    path("check_admin", views.check_admin, name="check_admin"),
]
