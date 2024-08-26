from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard,  name='dashboard'),
    path('create/', views.create_memory, name='create'),
    path('choose/', views.memory_choose, name='choose_memory')
]