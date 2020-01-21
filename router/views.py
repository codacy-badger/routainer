from django.shortcuts import render

from .models import Router
# Create your views here.
def index(request):
    rule_list = Router.objects.all()
    context = {'rule_list': rule_list}
    return render(request, 'router.html', context)