from django.contrib import admin

from .models import Llm, Token, Chat, Message

# Register your models here.
admin.site.register(Llm)
admin.site.register(Token)
admin.site.register(Chat, list_display=('title', 'user', 'created_on'))
admin.site.register(Message)