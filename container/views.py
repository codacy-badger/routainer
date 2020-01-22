from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Container
from router.models import Router


def index(request):
    container_list = Container.objects.all()
    context = {'container_list': container_list}
    return render(request, 'container.html', context)


def create(request):
    name = request.POST['ContainerName']
    domain = request.POST['ContainerDomain']
    port_config = request.POST['ContainerPort']
    ports = {
        'http': [],
        'stream': [],
    }

    if(port_config == 'default'):
        ports = {
            'http': [80],
            'stream': [22],
        }

    # add rules to router
    for p in ports['http']:
        rule = Router.create(name, p, 'http')
        rule.save()
    for p in ports['stream']:
        rule = Router.create(name, p, 'stream')
        rule.save()

    row = Container(name=name, domain=domain,
                    activity=False, exposed_port=ports)
    row.save()
    return HttpResponseRedirect(reverse('container:index'))


def delete(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    Router.objects.filter(container_name=container.name).delete()
    container.delete()
    return HttpResponseRedirect(reverse('container:index'))


def active(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    container.activity = True
    container.save()
    return HttpResponseRedirect(reverse('container:index'))


def inactive(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    container.activity = False
    container.save()
    return HttpResponseRedirect(reverse('container:index'))
