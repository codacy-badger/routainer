from django.db import models
import socket


class Router(models.Model):
    container_name = models.CharField(max_length=100)
    internal_port = models.IntegerField()
    external_port = models.IntegerField()
    port_type = models.CharField(max_length=20)

    @classmethod
    def create(cls, container, external_port, port_type):
        # get free internal port randomly
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        internal_port = tcp.getsockname()[1]
        tcp.close()

        return cls(container_name=container, internal_port=internal_port, external_port=external_port, port_type=port_type)