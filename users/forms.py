from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email", "username")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "username", 'first_name', 'last_name')

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ("username", "password")
    