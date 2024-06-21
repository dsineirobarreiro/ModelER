from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    
class Diagram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='name of the diagram', max_length=64, blank=True)
    elements = models.TextField(verbose_name='Data model elements', null=True)
    created_on = models.DateTimeField(verbose_name='date when the chat was created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(verbose_name='last time the diagram was accessed', auto_now=True)

    def __str__(self) -> str:
        return self.title

@receiver(pre_save, sender=Diagram)
def my_callback(sender, instance, *args, **kwargs):
    if not instance.title:
        count = sender.objects.filter(user=instance.user).count()
        index = '' if not count else ' (' + str(count) + ')'
        instance.title = 'Untitled diagram' + index

class Message(models.Model):
    index = models.IntegerField(verbose_name='message id inside the chat')
    content = models.TextField()
    timestamp = models.DateTimeField(verbose_name='time when the message was created', auto_now_add=True)
    choices = {
        'U': 'user',
        'A': 'assistant'
    }
    origin = models.CharField(max_length=1, choices=choices)
    diagram = models.ForeignKey(Diagram, on_delete=models.CASCADE)

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

def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/modeler/diagrams/{1}/{2}'.format(instance.diagram.user.id, instance.format, filename)

class FileQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.file.delete()
        super(FileQuerySet, self).delete(*args, **kwargs)

class Tool(models.Model):
    choices = {
        'P': 'Plantuml',
        'M': 'Mermaid'
    }
    value = models.CharField(max_length=1, choices=choices, unique=True)

    def __str__(self):
        return self.value

class File(models.Model):
    diagram = models.ForeignKey(Diagram, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    objects = FileQuerySet.as_manager()