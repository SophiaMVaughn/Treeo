from django.urls import path
from . import views

urlpatterns = [
    path('', views.patientlog, name='patientlog'),

]