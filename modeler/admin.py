from django.contrib import admin

from .models import Llm, Token, Chat, Message, File, Format

# Register your models here.
admin.site.register(Llm)
admin.site.register(Token)
admin.site.register(Chat, list_display=('title', 'user', 'created_on'))
admin.site.register(Message, list_display=('index', 'diagram', 'content', 'origin'))
admin.site.register(File, list_display=('file', 'format', 'diagram', 'software'))
admin.site.register(Format, list_display=('value',))