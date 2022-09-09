import base64
import json
import os

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods


@login_required
@require_GET
def only_limited_host(request: HttpRequest):
    host: str = request.get_host()
    if host == "example.com":  # ?????
        return render(request, "problems/success.html", {"flag": os.getenv("FLAG_O", "")})
    else:
        return render(request, "problems/error.html")


@login_required
@require_http_methods(["GET", "POST"])
def check_admin(request: HttpRequest):
    admin_cookie = request.COOKIES.get("exc")
    try:
        decoded_cookie = json.loads(base64.b64decode(admin_cookie).decode("utf-8"))
    except Exception:
        decoded_cookie = {"admin": False}
    is_admin = decoded_cookie["admin"]
    if request.method == "POST":
        message = {"admin": is_admin, "username": request.POST["username"]}
        response = render(request, "problems/exc.html", {"message": str(message)})
        cookie = json.dumps(message)
        response.set_cookie("exc", base64.b64encode(cookie.encode()).decode())
        return response
    if is_admin:
        message = os.getenv("FLAG_EXC")
    else:
        message = {"message": "please login any account."}

    return render(request, "problems/exc.html", {"message": str(message)})
