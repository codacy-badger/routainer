from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Container


def index(request):
    container_list = Container.objects.all()
    context = {'container_list': container_list}
    return render(request, 'container/index.html', context)


def create(request):
    name = request.POST['ContainerName']
    domain = request.POST['ContainerDomain']
    port_config = request.POST['ContainerPort']

    # setup ports
    ports = {
        'http': [],
        'stream': [],
    }

    if(port_config == 'default'):
        ports = {
            'http': [80],
            'stream': [22],
        }

    # create container
    row = Container.create(name=name, domain=domain, exposed_port=ports)
    row.save()
    return HttpResponseRedirect(reverse('container:index'))


def delete(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    container.destroy()
    return HttpResponseRedirect(reverse('container:index'))


def active(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    container.activate()
    return HttpResponseRedirect(reverse('container:index'))


def inactive(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    container.deactivate()
    return HttpResponseRedirect(reverse('container:index'))
