from .models import Llm, Chat
from asgiref.sync import async_to_sync

class LlmConverter:
    regex = "[a-zA-Z0-9]+"

    def to_python(self, value):
        return Llm.objects.filter(name=value).first()

    def to_url(self, value):
        return value

class DiagramConverter:
    regex = "[a-zA-Z0-9]+"

    def to_python(self, value):
        return Chat.objects.filter(pk=value).first()

    def to_url(self, value):
        return value.pk