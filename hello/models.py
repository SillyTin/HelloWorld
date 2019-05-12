from django.db import models

# Create your models here.

class FuncInfo(models.Model):
    addr = models.CharField(max_length = 32)
    name = models.CharField(max_length = 32)

class CallGraphEdge(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()

class CallGraphNode(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length = 32)