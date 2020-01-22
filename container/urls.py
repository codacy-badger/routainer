from django.urls import path

from . import views

app_name = 'container'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:container_id>/delete/', views.delete, name='delete'),
    path('<int:container_id>/active/', views.active, name='active'),
    path('<int:container_id>/inactive/', views.inactive, name='inactive'),
]
