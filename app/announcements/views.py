from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from users.models import User
from .models import Main, Announcement


class AnnouncementsView(LoginRequiredMixin, generic.ListView):
    template_name = 'announcements/announcements.html'
    context_object_name = 'announcements'
    queryset = Announcement.objects.all().order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        user: User = self.request.user
        user.points = user.total_score()

        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['main'] = Main.objects.first()

        return context
