from django.db import models


class Router(models.Model):
    container_name = models.CharField(max_length=100)
    internal_port = models.IntegerField()
    external_port = models.IntegerField()
    port_type = models.CharField(max_length=20)
