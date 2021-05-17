from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .models import User


class SignUpView(CreateView):
    form_class = UserCreationForm
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
        login(request, user)
        return redirect('/home/')

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        return render(request, 'users/signin.html', {'form': form, 'user': request.user})
