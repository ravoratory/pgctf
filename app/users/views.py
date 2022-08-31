from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import SignUpForm
from .models import User
from quizzes.models import Solved


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy('sites:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class SignInView(generic.View):
    def post(self, request, *arg, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'users/signin.html', {'form': form})
        username = form.cleaned_data.get('username')
        user = User.objects.get(username=username)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0

        form = AuthenticationForm(request.POST)
        return render(request, 'users/signin.html', {'form': form, 'user': request.user})


class UserDetailView(generic.DetailView):
    model = User
    template_name = "users/profile.html"
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['detail_user'] = self.object
        context['detail_user'].points = Solved.objects.filter(user=context['detail_user'], quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
        context['solved'] = Solved.objects.filter(user=self.object).select_related('quiz')

        if self.request.user.is_authenticated:
            context['user'].points = Solved.objects.filter(user=context['user'], quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0

        return context
