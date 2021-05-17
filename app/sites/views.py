from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.views import generic

from quizzes.models import Solved, Quiz, Solved


User = get_user_model()


class LandingPage(LoginRequiredMixin ,generic.View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
        quizzes = (Quiz.objects
            .select_related('category')
            .filter(published=True)
            .order_by('quiz_number')
            .annotate(is_solved=Count('solved_users', filter=Q(solved__user=request.user)))
        )

        return render(request, 'sites/home.html', {'user': user, 'quizzes': quizzes})
