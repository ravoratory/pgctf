from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Sum

from app.quizzes.models import Solved
from .models import Main, Announcement


class AnnouncementsView(LoginRequiredMixin, generic.ListView):
    template_name = 'announcements/announcements.html'
    context_object_name = 'announcements'
    queryset = Announcement.objects.all().order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = Main.objects.first()
        user = self.request.user
        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
        context['user'] = user
        return context
