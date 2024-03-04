import asyncio
import json
from django.http import HttpResponseBadRequest, JsonResponse

from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings

from .forms import ModelForm

async def process_prompt(prompt):
    await asyncio.sleep(5)
    """generate = settings.LLM
    result = json.loads(generate(prompt))"""
    result = json.loads("""{"entities":[{"name":"Client","attributes":["name","email","phone"]},{"name":"Bank","attributes":["name","branch","contact"]},{"name":"Transaction","attributes":["id","account","date","amount"]}],"relations":[{"source":"Client","target":"Bank","name":"client_bank"},{"source":"Bank","target":"Transaction","name":"bank_transaction"}]}""")
    print(result)
    diagram = {}
    for entity in result['entities']:
        aux = []
        for key in entity.get("attributes"):
            aux.append(key)
        diagram[entity["name"]] = aux
    return diagram

class IndexView(TemplateView):
    template_name = "modeler/index.html"

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class ModelView(TemplateView):
    form_class = ModelForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"
    stop = False

    async def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                loop = asyncio.get_event_loop()
                diagram = await loop.create_task(process_prompt(prompt))
                return JsonResponse(diagram)
        else:
            return HttpResponseBadRequest('Invalid request')

class DiagramView(TemplateView):
    template_name = 'modeler/diagram.html'
    form_class = ModelForm
    not_loaded = True

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'not_loaded': self.not_loaded})
    
    async def post(self, request):
        return JsonResponse({'status': 'ok'})