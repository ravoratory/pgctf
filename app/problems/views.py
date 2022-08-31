from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpRequest


@login_required
@require_GET
def only_invalid_ip(request: HttpRequest):
    host: str = request.get_host().split(':')[0]
    if host == '123.456.789.123':  # ?????
        return render(request, 'problems/success.html')
    else:
        return render(request, 'problems/error.html', {'host': host})
