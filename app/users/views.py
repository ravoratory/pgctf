from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from common.views import UserContextMixin
from quizzes.models import Solved

from .forms import SignUpForm
from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("sites:home")
    template_name = "users/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class SignInView(UserContextMixin, generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("sites:home")
    template_name = "users/signin.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        user = User.objects.get(username=username)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        return super().form_valid(form)


class UserDetailView(UserContextMixin, LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/profile.html"
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_user"] = self.object
        context["detail_user"].points = context["detail_user"].total_score()
        context["solved"] = Solved.objects.filter(user=self.object).select_related("quiz")

        return context
