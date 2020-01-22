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

    row = Router.create(container, port, rule_type)
    row.save()
    return HttpResponseRedirect(reverse('router:index'))


def delete(request, rule_id):
    rule = get_object_or_404(Router, pk=rule_id)
    rule.delete()
    return HttpResponseRedirect(reverse('router:index'))
