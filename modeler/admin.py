from django.contrib import admin

from .models import Llm, Token

# Register your models here.
admin.site.register(Llm)
admin.site.register(Token)