import asyncio
import json
from django.http import HttpResponseBadRequest, JsonResponse

from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from .forms import PromptForm

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