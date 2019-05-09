from django.db import models

# Create your models here.

class FuncInfo(models.Model):
    addr = models.CharField(max_length = 32)
    name = models.CharField(max_length = 32)