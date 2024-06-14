from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
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
        next = request.GET['next']
        return render(request, self.template_name, {'form': form, 'next': next})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        next = request.GET['next']
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect(request.GET['next'])
        else:
            return render(request, self.template_name, {'form': form, 'next': next})

class CustomPasswordChangeView(PasswordChangeView):
    template_name='registration/password_change.html'
    success_url = reverse_lazy('users:password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='registration/password_done.html'