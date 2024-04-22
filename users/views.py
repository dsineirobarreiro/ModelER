from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth import views
from django.conf import settings

from .forms import LoginForm, SignupForm

class CustomLoginView(views.LoginView):
    authentication_form = LoginForm
    

class SignupView(TemplateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect(request.GET['next'])
        else:
            return render(request, self.template_name, {'form': form})
