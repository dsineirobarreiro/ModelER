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
    title = models.CharField(verbose_name='name of the diagram', max_length=64, default='Untitled diagram', unique=True)
    created_on = models.DateTimeField(verbose_name='date when the chat was created', auto_now_add=True)

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