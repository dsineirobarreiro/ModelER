import asyncio
import httpx

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from django.urls import reverse

from .forms import PromptForm
from .models import Llm, Token

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

class ModelOptionView(ListView):
    model = Llm
    template_name = 'modeler/model_option.html'

class ModelView(TemplateView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"

    async def get(self, request, *args, **kwargs):
        llm = await Llm.objects.filter(name=kwargs.get('llm')).afirst()
        form = self.form_class(initial=self.initial)
        user = await request.auser()
        token = True
        if llm and not llm.open_source:
            if user.is_authenticated:
                token = await Token.objects.filter(user=user, llm=llm).afirst()
            else:
                token = False
        return render(request, self.template_name, {'user': user,'form': form, 'llm': llm, 'token': token})

    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        llm = await Llm.objects.aget(name=kwargs.get('llm'))

        if form.is_valid():
            print(form.cleaned_data, llm)
            headers = {'ngrok-skip-browser-warning': 'true'}
            async def process_response():
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        "POST",
                        "http://localhost:8001/test/",
                        headers=headers,
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
        section = kwargs.get('section', 'general')
        active = [
            'active' if section == 'general' else '',
            'active' if section == 'settings' else '',
            'active' if section == 'diagrams' else '',
            'active' if section == 'tokens' else ''
        ]
        active.reverse()
        return render(request, self.template_name, {'user': user, 'section': section, 'active': active})