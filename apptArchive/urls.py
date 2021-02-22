from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_archived_appointment, name='apptArchive'),

]