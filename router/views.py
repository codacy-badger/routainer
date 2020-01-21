from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Router


def index(request):
    rule_list = Router.objects.all()
    context = {'rule_list': rule_list}
    return render(request, 'router.html', context)


def create(request):
    return HttpResponseRedirect(reverse('router:index'))
