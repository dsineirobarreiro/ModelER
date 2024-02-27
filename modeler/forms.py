from django import forms


class ModelForm(forms.Form):
    """choices = (('mistral', 'Mistral'), ('llama2', 'LlaMa2'),)
    model = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(attrs={'class': 'flex model-sel flex-even'}))"""
    prompt = forms.CharField(label="Describe your scenario", widget=forms.Textarea(attrs={'cols': 60, 'rows': 1, 'placeholder': 'Type your prompt'}))