from django import forms

from .models import Chat, File, Token


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Describe your scenario', widget=forms.Textarea(attrs={'cols': 60, 'rows': 1, 'placeholder': 'Type your prompt'}))

class DiagramForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['title']

class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['value']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'software']