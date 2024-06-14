from django.db import models

from users.models import User

# Create your models here.
class Llm(models.Model):
    name = models.CharField(verbose_name='model name', max_length=128, unique=True)
    open_source = models.BooleanField(verbose_name='open source')

    def __str__(self) -> str:
        return self.name

class Token(models.Model):
    value = models.TextField(verbose_name='API token for the model')
    llm = models.ForeignKey(Llm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.value
    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='name of the diagram', max_length=64, default='Untitled diagram')
    created_on = models.DateTimeField(verbose_name='date when the chat was created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(verbose_name='last time the diagram was accessed', auto_now=True)

    def __str__(self) -> str:
        return self.title

class Message(models.Model):
    index = models.IntegerField(verbose_name='message id inside the chat')
    content = models.TextField()
    timestamp = models.DateTimeField(verbose_name='time when the message was created', auto_now_add=True)
    choices = {
        'U': 'user',
        'A': 'assistant'
    }
    origin = models.CharField(max_length=1, choices=choices)
    diagram = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.content
    
    @classmethod
    def next_index(cls, diagram):
        last_message = cls.objects.filter(diagram=diagram).last()
        if not last_message:
            return 0
        return last_message.index + 1

class Format(models.Model):
    choices = {
        'png': 'png',
        'svg': 'svg'
    }
    value = models.CharField(max_length=3, choices=choices, unique=True)

    def __str__(self):
        return self.value

class File(models.Model):
    diagram = models.ForeignKey(Chat, on_delete=models.CASCADE)
    file = models.FileField(upload_to='modeler/diagrams/')
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    choices = {
        'G': 'Gojs',
        'P': 'Plantuml',
        'M': 'Mermaid'
    }
    software = models.CharField(max_length=1, choices=choices)