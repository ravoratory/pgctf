from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from common.views import UserContextMixin

from .models import Announcement, Main


class AnnouncementsView(UserContextMixin, LoginRequiredMixin, generic.ListView):
    template_name = "announcements/announcements.html"
    context_object_name = "announcements"
    queryset = Announcement.objects.all().order_by("-created_at")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main"] = Main.objects.first()

        return context
