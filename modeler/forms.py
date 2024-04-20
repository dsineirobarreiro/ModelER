from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Describe your scenario', widget=forms.Textarea(attrs={'cols': 60, 'rows': 1, 'placeholder': 'Type your prompt'}))