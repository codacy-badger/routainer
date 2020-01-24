from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Container
from router.models import Router

import lxc


def index(request):
    container_list = Container.objects.all()
    context = {'container_list': container_list}
    return render(request, 'container/index.html', context)


def create(request):
    name = request.POST['ContainerName']
    domain = request.POST['ContainerDomain']
    port_config = request.POST['ContainerPort']

    # Setup the container object
    c = lxc.Container(name)
    # Create the container rootfs
    c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                "release": "bionic",
                                                "arch": "amd64"})
    # Install OpenSSH Server
    c.attach_wait(lxc.attach_run_command,
                  ["apt-get", "update"])
    c.attach_wait(lxc.attach_run_command,
                  ["apt-get", "upgrade", "-y"])
    c.attach_wait(lxc.attach_run_command,
                  ["apt-get", "install", "openssh-server", "-y"])

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

    # add rules to router
    for p in ports['http']:
        rule = Router.create(name, p, 'http')
        rule.save()
    for p in ports['stream']:
        rule = Router.create(name, p, 'stream')
        rule.save()

    # create container
    row = Container(name=name, domain=domain,
                    activity=False, exposed_port=ports)
    row.save()
    return HttpResponseRedirect(reverse('container:index'))


def delete(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    Router.objects.filter(container_name=container.name).delete()
    c = lxc.Container(container.name)
    c.destroy()
    container.delete()
    return HttpResponseRedirect(reverse('container:index'))


def active(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    c = lxc.Container(container.name)
    c.start()
    container.activity = (
        container.state == "STARTING" or container.state == "RUNNING")
    container.save()
    return HttpResponseRedirect(reverse('container:index'))


def inactive(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    c = lxc.Container(container.name)
    c.stop()
    container.activity = (
        container.state == "STOPPING" or container.state == "STOPPED")
    container.save()
    return HttpResponseRedirect(reverse('container:index'))
