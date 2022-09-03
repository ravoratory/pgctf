import json

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Max, Sum, When, Case
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from datetime import datetime

from quizzes.models import Solved

User = get_user_model()


@require_GET
def ranking_page(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0

    ranking = (User.objects
        .filter(is_active=True, is_staff=False)
        .prefetch_related('solved')
        .annotate(points=Sum(Case(When(solved__solved_datetime__lt=datetime(2022, 9, 10), then='solved__quiz__point'))))
        .annotate(rank=Window(
            expression=Rank(),
            order_by=F('points').desc(nulls_last=True),
        ))
        .annotate(last_solve=Max('solved__solved_datetime'))
        .values('rank', 'username', 'points', 'last_solve')
        .order_by('rank', 'last_solve')
    )
    print(ranking)
    return render(request, 'sites/ranking.html', {'user': user, 'ranking': ranking})


@require_GET
def ranking_chart(request, *args, **kwargs):
    limit = request.GET.get('limit', 10)

    ranking = (User.objects
        .filter(is_active=True, is_staff=False)
        .prefetch_related('solved')
        .filter(solved__solved_datetime__lt=datetime(2022, 9, 10))
        .annotate(points=Sum('solved__quiz__point'))
        .annotate(rank=Window(
            expression=Rank(),
            order_by=F('points').desc(nulls_last=True),
        ))
        .annotate(last_solve=Max('solved__solved_datetime'))
        .order_by('rank', 'last_solve')
        .values('id')
    )[:limit]
    solved = (Solved.objects.filter(user__in=ranking)
        .annotate(date_joined=F('user__date_joined'))
        .annotate(username=F('user__username'))
        .annotate(point=F('quiz__point'))
        .values('username', 'point', 'solved_datetime', 'date_joined')
        .order_by('solved_datetime')
    )

    users = {}
    times = []
    for record in solved:
        if users.get(record['username']) is None:
            users[record['username']] = []
            times.append({
                'time': record['date_joined'],
                'username': record['username'],
                'point': 0,
            })

        for t in times:
            if t['username'] == record['username']:
                point = t['point']

        times.append({
            'time': record['solved_datetime'],
            'username': record['username'],
            'point': record['point'] + point,
        })
    times.sort(key=lambda k: k['time'])

    response = {'datetime': [], 'points': users, 'usernames': list(users.keys())}
    for time in times:
        response['datetime'].append(time['time'])
        for u in users.keys():
            if u == time['username']:
                response['points'][u].append(time['point'])
            else:
                response['points'][u].append('NaN')

    response = json.dumps(response, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')
