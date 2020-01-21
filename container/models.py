from django.db import models

# Create your models here.
class Container(models.Model):
    name = models.CharField(max_length=16)
    domain = models.CharField(max_length=100)
    activity = models.BooleanField()
    exposed_port = models.CharField(max_length=200)