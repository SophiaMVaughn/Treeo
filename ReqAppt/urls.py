from django.urls import path, include
from ReqAppt import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('Doctor', views.Doctor_view),
    path('Patient', views.Patient_view),
    path('Admin', views.Admin_view),
    path('Appointment', views.Appointment_view),
    path('Pending', views.Pending),
    path('delete/<int:id>', views.Destroy),
]
