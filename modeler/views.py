import asyncio
import httpx

from django.http import JsonResponse, StreamingHttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PromptForm, DiagramForm, FileForm, TokenForm
from .models import Llm, Token, Chat, Message, File, Format

from users.forms import UserChangeForm

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

class DiagramSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/diagram_selection.html'

    def post(self, request, *args, **kwargs):
        diagram = Chat(user=request.user)
        diagram.save()
        return redirect(reverse(f'modeler:model', kwargs={'llm': 'llama2', 'pk': diagram}))

class ModelView(LoginRequiredMixin, FormView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"

    def get(self, request, *args, **kwargs):
        llm = self.kwargs['llm']
        diagram = kwargs['pk']
        diagram.save()
        token = True
        if not llm.open_source:
            token = Token.objects.filter(user=self.request.user, llm=llm).first()
        token = True if token else False
        form = self.form_class(initial=self.initial)
        message_list = Message.objects.filter(diagram=diagram)
        files = []
        for file in File.objects.filter(diagram=diagram):
            files.append(file)
        return render(request, self.template_name, {'llm': llm, 'diagram': diagram, 'token': token, 'form': form, 'message_list': message_list, 'files': files})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            user_message = Message(index=Message.next_index(kwargs['pk']), content=prompt, origin='U', diagram=kwargs['pk'])
            user_message.save()

            headers = {'ngrok-skip-browser-warning': 'true'}
            
            def generate(headers, form):
                def process_response():
                    msg = ''
                    with httpx.Client(timeout=None) as client:
                        with client.stream(
                            "POST",
                            "http://localhost:8001/llama/greet/",
                            headers=headers,
                            data=form
                        ) as r:
                            for text in r.iter_text():
                                # Work on chunk and then stream it
                                msg += text
                                yield text
                    message = Message(index=Message.next_index(kwargs['pk']), content=msg, origin='A', diagram=kwargs['pk'])
                    message.save()

                    
                return StreamingHttpResponse(
                    process_response()
                )
                
            return generate(headers, form.cleaned_data)

class ProfileGeneralView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/profile/general.html'

    def get(self, request, *args, **kwargs):
        active = {
            'general': 'active',
            'settings': '',
            'diagrams': '',
            'tokens': ''
        }
        return render(request, self.template_name, {'active': active})

class ProfileSettingsView(LoginRequiredMixin, FormView):
    template_name = 'modeler/profile/settings.html'
    form_class = UserChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.request.user)
        active = {
            'general': '',
            'settings': 'active',
            'diagrams': '',
            'tokens': ''
        }
        context['active'] = active
        context['form'] = form

        return context

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
        return render(request, self.template_name, self.get_context_data())

class ProfileDiagramsView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/profile/diagrams.html'

    def get(self, request, *args, **kwargs):
        active = {
            'general': '',
            'settings': '',
            'diagrams': 'active',
            'tokens': ''
        }
        diagrams = Chat.objects.filter(user=request.user)
        return render(request, self.template_name, {'active': active, 'diagramset': diagrams})

class ProfileTokensView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/profile/tokens.html'

    def get(self, request, *args, **kwargs):
        active = {
            'general': '',
            'settings': '',
            'diagrams': '',
            'tokens': 'active'
        }
        tokens = Token.objects.filter(user=request.user)
        return render(request, self.template_name, {'active': active, 'tokens': tokens})

class DiagramView(LoginRequiredMixin, FormView):
    form_class = DiagramForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            diagram = self.kwargs['pk']
            diagram.title = title
            diagram.save()
            return JsonResponse({'msg': 'Successfull'})
        else:
            return HttpResponseBadRequest({'error': 'Form not valid'})

class TokenView(LoginRequiredMixin, FormView):
    form_class = TokenForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            token = self.kwargs['pk']
            token.value = value
            token.save()
            return JsonResponse({'msg': 'Successfull'})
        else:
            return HttpResponseBadRequest({'error': 'Form not valid'})

class DiagramDownloadView(LoginRequiredMixin, FormView):
    form_class = FileForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file_content = form.cleaned_data['file']
            software = form.cleaned_data['software']
            diagram = self.kwargs['pk']
            format = Format.objects.filter(value=kwargs['format']).first()
            if not format:
                return HttpResponseBadRequest({'error': 'Form not valid'})
            file = File(diagram=diagram, format=format, file=file_content, software=software)
            file.save()
            return JsonResponse({'msg': 'Successfull'})
        else:
            return HttpResponseBadRequest({'error': 'Form not valid'})