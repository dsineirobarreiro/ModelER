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