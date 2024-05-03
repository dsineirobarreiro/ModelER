import asyncio
import httpx

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from django.urls import reverse

from .forms import PromptForm
from .models import Llm

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
        llm = await Llm.objects.aget(name=kwargs.get('llm'))
        form = self.form_class(initial=self.initial)
        user = await request.auser()
        return render(request, self.template_name, {'user': user,'form': form, 'llm': llm})

    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        llm = await Llm.objects.aget(name=kwargs.get('llm'))

        if form.is_valid():
            #prompt = form.cleaned_data['prompt']
            print(form.cleaned_data, llm)
            headers = {'ngrok-skip-browser-warning': 'true'}
            #with httpx.stream("GET", "https://f6a2-104-155-129-7.ngrok-free.app/greet/", headers=headers) as r:
            #    for text in r.iter_text():
            #        print(text)
                #return StreamingHttpResponse(stream_response(r.aiter_lines()), content_type='text/event-stream')
            async def process_response():
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        "GET",
                        "https://f6a2-104-155-129-7.ngrok-free.app/greet/",
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
        return render(request, self.template_name, {'user': user})