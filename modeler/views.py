import asyncio
import json
from django.http import HttpResponseBadRequest, JsonResponse

from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from .forms import *
from .utils import create_mermaid_diagram, create_uml_diagram

class IndexView(TemplateView):
    template_name = "modeler/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class ModelView(TemplateView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

"""    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                loop = asyncio.get_event_loop()
                diagram = await loop.create_task(process_prompt(prompt))
                return JsonResponse(diagram)
        else:
            return HttpResponseBadRequest('Invalid request')"""

class LoginView(TemplateView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('modeler:index')
        else:
            return render(request, self.template_name, {'form': form})

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
            form.save()
            return redirect('modeler:login')
        else:
            return render(request, self.template_name, {'form': form})