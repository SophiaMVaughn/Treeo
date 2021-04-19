from django.urls import path
from . import views

urlpatterns = [
    path('', views.test2, name='messaging_home'),
]
