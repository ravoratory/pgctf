from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Max, Q, Sum
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.shortcuts import render
from django.views.decorators.http import require_GET

from quizzes.models import Quiz, Solved

User = get_user_model()


@login_required
@require_GET
def LandingPage(request, *args, **kwargs):
    user = request.user
    user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
    quizzes = (Quiz.objects
        .select_related('category')
        .filter(published=True)
        .order_by('quiz_number')
        .annotate(is_solved=Count('solved_users', filter=Q(solved__user=request.user)))
    )

    return render(request, 'sites/home.html', {'user': user, 'quizzes': quizzes})


@require_GET
def ranking_page(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0

    ranking = (User.objects
        .filter(is_active=True, is_staff=False)
        .prefetch_related('solved')
        .annotate(points=Sum('solved__quiz__point'))
        .annotate(rank=Window(
            expression=Rank(),
            order_by=F('points').desc(nulls_last=True),
        ))
        .annotate(last_solve=Max('solved__solved_datetime'))
        .values('rank', 'username', 'points', 'last_solve')
        .order_by('rank', '-last_solve')
    )

    return render(request, 'sites/ranking.html', {'user': user, 'ranking': ranking})
