from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q, Sum
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
        .filter(is_active=True)#, is_staff=False)
        .prefetch_related('solved')
        .annotate(points=Sum('solved__quiz__point'))
        .order_by('-date_joined')
        .values('username', 'points', 'date_joined')
        .order_by(F('points').desc(nulls_last=True), '-date_joined')
    )

    return render(request, 'sites/ranking.html', {'user': user, 'ranking': ranking})
