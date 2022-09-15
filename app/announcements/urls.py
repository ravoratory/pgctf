from django.urls import path

from . import views

app_name = "announcements"
urlpatterns = [
    path("", views.AnnouncementsView.as_view(), name="announcements"),
]
