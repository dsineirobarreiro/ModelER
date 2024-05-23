from .models import Llm
from asgiref.sync import async_to_sync

class LlmConverter:
    regex = "[a-zA-Z0-9]+"

    def to_python(self, value):
        return Llm.objects.filter(name=value).afirst()

    def to_url(self, value):
        return value