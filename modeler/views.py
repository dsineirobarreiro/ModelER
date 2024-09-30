import asyncio
import httpx

from django.http import JsonResponse, QueryDict, StreamingHttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PromptForm, DiagramForm, FileForm, TokenForm
from .models import Llm, Token, Diagram, Message, File, Format, Tool

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
        

class IndexView(TemplateView):
    template_name = "modeler/index.html"

async def stream_response(response):
    # Generate data in chunks
    async for chunk in response:
        yield chunk

class ModelListView(ListView):
    model = Llm
    template_name = 'modeler/model_list.html'

    def post(self, request, *args, **kwargs):
        diagram = Diagram(user=request.user, title=request.POST['title'])
        diagram.save()
        return redirect(reverse(f'modeler:model', kwargs={'llm': 'llama2', 'pk': diagram}))

class DiagramSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'modeler/diagram_selection.html'

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
        message_list = Message.objects.filter(diagram=diagram).order_by()
        files = {}
        formats = Format.objects.all()
        tools = Tool.objects.all()
        for format in formats:
            files[format.value] = {}
            for tool in tools: 
                file = File.objects.filter(diagram=diagram, format=format, tool=tool).last()
                if file:
                    files[format.value][tool.get_value_display()] = file.file.url
        return render(request, self.template_name, {
            'llm': llm,
            'diagram': diagram,
            'token': token,
            'form': form,
            'message_list': message_list,
            'files': files,
            'plant': files['png'].get('Plantuml', '#'),
            'mermaid': files['svg'].get('Mermaid',''),
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            action = form.cleaned_data['action']
            print(action)
            user_message = Message(index=Message.next_index(kwargs['pk']), content=prompt, origin='U', diagram=kwargs['pk'])
            user_message.save()

            headers = {'ngrok-skip-browser-warning': 'true'}
            
            def generate(headers, form):
                def process_response():
                    msg = ''
                    with httpx.Client(timeout=None) as client:
                        with client.stream(
                            "POST",
                            f"https://bright-akita-pleasantly.ngrok-free.app/llama2/{action}/",
                            headers=headers,
                            data=form
                        ) as r:
                            for text in r.iter_text():
                                # Work on chunk and then stream it
                                msg += text
                                yield text
                    diagram = kwargs['pk']
                    print(msg)
                    message = Message(index=Message.next_index(kwargs['pk']), content=msg, origin='A', diagram=diagram)
                    message.save()
                    diagram.elements = msg
                    diagram.save()

                    
                return StreamingHttpResponse(
                    process_response()
                )
                
            return generate(headers, form.cleaned_data)
        else:
            def error():
                error_message = 'Sorry, a bad response was obtained from the server. Try again please.'
                for string in error_message:
                    yield string
            return StreamingHttpResponse(error())

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
        diagrams = Diagram.objects.filter(user=request.user)
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
        post_dict = request.POST.copy()
        post_dict['tool'] = Tool.objects.filter(value=request.POST['tool']).first()
        form = self.form_class(post_dict, request.FILES)
        if form.is_valid():
            file_content = form.cleaned_data['file']
            tool = form.cleaned_data['tool']
            diagram = self.kwargs['pk']
            format = Format.objects.filter(value=kwargs['format']).first()
            if not format:
                return HttpResponseBadRequest({'error': 'Form not valid'})
            file = File(diagram=diagram, format=format, file=file_content, tool=tool)
            file.save()
            return JsonResponse({'path': file.file.url, 'tool': file.tool.get_value_display(), 'format': file.format.value})
        else:
            return HttpResponseBadRequest({'error': 'Form not valid'})