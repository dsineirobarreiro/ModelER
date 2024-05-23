import asyncio
import httpx

from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.base import RedirectView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from asgiref.sync import async_to_sync

from .forms import PromptForm
from .models import Llm, Token, Chat

async def stream_data():
    # Generate data in chunks
    for i in "Hi, I am here to help you model your E/R Diagram!$":
        yield f'data: {i}\n\n'
        # Simulate delay between chunks
        await asyncio.sleep(.05)

async def stream_http(request):
    response = StreamingHttpResponse(stream_data())
    response['Content-Type'] = 'text/event-stream'
    return response

class StreamView(TemplateView):
    template_name = "modeler/stream.html"

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
        

class IndexView(TemplateView):
    template_name = "modeler/index.html"

async def stream_response(response):
    # Generate data in chunks
    async for chunk in response:
        yield chunk

class ModelListView(ListView):
    model = Llm
    template_name = 'modeler/model_list.html'

class DiagramView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/diagram.html'

    def post(self, request, *args, **kwargs):
        diagram = Chat(user=request.user)
        diagram.save()
        return redirect(reverse(f'modeler:model', kwargs={'llm': 'llama2', 'title': diagram}))

        

class CreateDiagramView(RedirectView):
    pattern_name = 'modeler:model'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect(reverse(f"{settings.LOGIN_URL}") + f'?next={self.request.path}')
        diagram = Chat(user=user)
        diagram.save()
        kwargs['pk'] = diagram.pk
        return super().get_redirect_url(*args, **kwargs)


class ModelView(LoginRequiredMixin, FormView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['llm'] = self.kwargs['llm']
        token = True
        if not context['llm'].open_source:
            token = Token.objects.filter(user=self.request.user, llm=context['llm']).first()
        context['token'] = True if token else False
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        llm = kwargs.get('llm')

        if form.is_valid():
            print(form.cleaned_data, llm)
            headers = {'ngrok-skip-browser-warning': 'true'}
            
            def generate(headers, form):
                def process_response():
                    with httpx.Client(timeout=None) as client:
                        with client.stream(
                            "POST",
                            "http://localhost:8001/llama2/generate/",
                            headers=headers,
                            data=form
                        ) as r:
                            for text in r.iter_text():
                                # Work on chunk and then stream it
                                yield text

                    
                return StreamingHttpResponse(
                    process_response()
                )
                
            return generate(headers, form.cleaned_data)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/profile.html'

    def get(self, request, *args, **kwargs):
        section = kwargs.get('section', 'general')
        active = [
            'active' if section == 'general' else '',
            'active' if section == 'settings' else '',
            'active' if section == 'diagrams' else '',
            'active' if section == 'tokens' else ''
        ]
        active.reverse()
        return render(request, self.template_name, {'section': section, 'active': active})