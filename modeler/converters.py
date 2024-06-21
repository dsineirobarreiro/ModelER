from .models import Llm, Diagram, Token

class LlmConverter:
    regex = "[a-zA-Z0-9]+"

    def to_python(self, value):
        return Llm.objects.filter(name=value).first()

    def to_url(self, value):
        return value

class DiagramConverter:
    regex = "[a-zA-Z0-9]+"

    def to_python(self, value):
        return Diagram.objects.filter(pk=value).first()

    def to_url(self, value):
        return value.pk

class TokenConverter:
    regex = ".+"

    def to_python(self, value):
        return Token.objects.filter(pk=value).first()

    def to_url(self, value):
        return value.pk
    