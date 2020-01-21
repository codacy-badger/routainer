from django.shortcuts import render

from .models import Container

# Create your views here.
def index(request):
    container_list = Container.objects.all()
    context = {'container_list': container_list}
    return render(request, 'container.html', context)