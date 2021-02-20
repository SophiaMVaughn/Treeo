
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Health_Coach, name='Health_Coach'),
    path('Provider', views.provider, name='provider'),
    path('Dietitian', views.dietitian, name='dietitian'),
]