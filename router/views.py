from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Router


def index(request):
    rule_list = Router.objects.all()
    context = {'rule_list': rule_list}
    return render(request, 'router/index.html', context)


def create(request):
    container = request.POST['RuleContainer']
    port = request.POST['RulePort']
    rule_type = request.POST['RuleType']

    rule = Router.create(container, port, rule_type)
    rule.applyAndReload()
    return HttpResponseRedirect(reverse('router:index'))


def delete(request, rule_id):
    rule = get_object_or_404(Router, pk=rule_id)
    rule.destroyAndReload()
    return HttpResponseRedirect(reverse('router:index'))
