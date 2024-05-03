from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Llm(models.Model):
    name = models.CharField(verbose_name='model name', max_length=128, unique=True)
    open_source = models.BooleanField(verbose_name='open source')

    def __str__(self) -> str:
        return self.name