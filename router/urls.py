from django.urls import path

from . import views

app_name = 'router'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:rule_id>/delete/', views.delete, name='delete'),
]
