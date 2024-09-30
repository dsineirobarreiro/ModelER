from django import forms

from .models import Diagram, File, Token


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Describe your scenario', widget=forms.Textarea(attrs={'cols': 58, 'rows': 1, 'placeholder': 'Type your prompt'}))
    action = forms.CharField()

class DiagramForm(forms.ModelForm):
    class Meta:
        model = Diagram
        fields = ['title']

class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['value']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'tool']