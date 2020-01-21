from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Container


def index(request):
    container_list = Container.objects.all()
    context = {'container_list': container_list}
    return render(request, 'container.html', context)


def create(request):
    return HttpResponseRedirect(reverse('container:index'))
