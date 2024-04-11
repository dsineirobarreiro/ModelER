import asyncio
import json
from django.http import HttpResponseBadRequest, JsonResponse

from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings

from .forms import ModelForm
from .utils import create_mermaid_diagram, create_uml_diagram

async def process_prompt(prompt):
    await asyncio.sleep(5)
    generate = settings.LLM
    result = json.loads(generate(prompt))
    #result = json.loads("""{"entities": [{"name": "Customer", "attributes": [{"name": "customer_id", "type": "integer"}, {"name": "first_name", "type": "string"}, {"name": "last_name", "type": "string"}, {"name": "email", "type": "string"}, {"name": "phone_number", "type": "string"}]}, {"name": "Order", "attributes": [{"name": "order_id", "type": "integer"}, {"name": "customer_id", "type": "integer"}, {"name": "order_date", "type": "date"}, {"name": "total_amount", "type": "decimal"}]}, {"name": "Product", "attributes": [{"name": "product_id", "type": "integer"}, {"name": "product_name", "type": "string"}, {"name": "price", "type": "decimal"}]}], "relations": [{"name": "customer_orders", "source": "Customer", "target": "Order", "cardinality_of_source": "One or Many", "cardinality_of_target": "One or Many"}, {"name": "order_products", "source": "Order", "target": "Product", "cardinality_of_source": "One or Many", "cardinality_of_target": "One or Many"}]}""")
    print(result)
    diagram = {
        'raw': result,
        'mermaid': create_mermaid_diagram(result),
        'uml': create_uml_diagram(result)
    }
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
    template_name = 'modeler/login.html'
    