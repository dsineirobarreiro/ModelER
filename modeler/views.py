import asyncio
import httpx

from django.http import StreamingHttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.base import RedirectView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from asgiref.sync import sync_to_async

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

    async def get(self, request, *args, **kwargs):
        user = await request.auser()
        return render(request, self.template_name, {'user': user})


async def stream_response(response):
    # Generate data in chunks
    async for chunk in response:
        yield chunk

class ModelListView(ListView):
    model = Llm
    template_name = 'modeler/model_list.html'

class DiagramView(TemplateView):
    template_name = 'modeler/diagram.html'

    async def get(self, request, *args, **kwargs):
        user = await request.auser()
        if not user.is_authenticated:
            return redirect(reverse(f"{settings.LOGIN_URL}") + f'?next={request.path}')
        llm = await Llm.objects.filter(name=kwargs.get('llm')).afirst()
        return render(request, self.template_name, {'user': user, 'llm': llm})

    async def post(self, request, *args, **kwargs):
        user = await request.auser()
        if not user.is_authenticated:
            pass #devolver invalid request o algo
        diagram = Chat(user=user)
        await diagram.asave()
        return redirect(reverse(f'modeler:model', kwargs={'llm': 'llama2', 'pk': diagram.pk}))

        

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

class ModelView(TemplateView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"
    

    async def get(self, request, *args, **kwargs):
        user = await request.auser()
        if not user.is_authenticated:
            return redirect(reverse(f"{settings.LOGIN_URL}") + f'?next={request.path}')
        print(type(kwargs.get('llm')))
        llm = await Llm.objects.filter(name=kwargs.get('llm')).afirst()
        form = self.form_class(initial=self.initial)
        token = True
        if llm and not llm.open_source:
            if user:
                token = await Token.objects.filter(user=user, llm=llm).afirst()
            else:
                token = False
        return render(request, self.template_name, {'user': user,'form': form, 'llm': llm, 'token': token})

    async def post(self, request, *args, **kwargs):
        user = await request.auser()
        if not user.is_authenticated:
            pass #devolver invalid request o algo
        form = self.form_class(request.POST)
        llm = await Llm.objects.aget(name=kwargs.get('llm'))

        if form.is_valid():
            print(form.cleaned_data, llm)
            headers = {'ngrok-skip-browser-warning': 'true'}
            async def process_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream(
                        "POST",
                        "http://localhost:8001/llama2/generate/",
                        headers=headers,
                        data=form.cleaned_data
                    ) as r:
                        async for text in r.aiter_text():
                            # Work on chunk and then stream it
                            yield text

                
            return StreamingHttpResponse(
                process_response()
            )

class ProfileView(TemplateView):
    template_name = 'modeler/profile.html'

    async def get(self, request, *args, **kwargs):
        user = await request.auser()
        if not user.is_authenticated:
            return redirect(reverse(f"{settings.LOGIN_URL}") + f'?next={request.path}')
        section = kwargs.get('section', 'general')
        active = [
            'active' if section == 'general' else '',
            'active' if section == 'settings' else '',
            'active' if section == 'diagrams' else '',
            'active' if section == 'tokens' else ''
        ]
        active.reverse()
        return render(request, self.template_name, {'user': user, 'section': section, 'active': active})