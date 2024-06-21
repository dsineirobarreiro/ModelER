from django.contrib import admin

from .models import Llm, Token, Diagram, Message, File, Format, Tool

# Register your models here.
admin.site.register(Llm)
admin.site.register(Token)
admin.site.register(Diagram, list_display=('title', 'user', 'created_on'))
admin.site.register(Message, list_display=('index', 'diagram', 'content', 'origin'))
admin.site.register(File, list_display=('file', 'format', 'diagram', 'tool'))
admin.site.register(Format, list_display=('value',))
admin.site.register(Tool, list_display=('value',))