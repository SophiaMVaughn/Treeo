from django.urls import path, include
from ReqAppt import views

urlpatterns = [
    path('', views.home),
    path('home', views.home, name='reqAppt'),
    path('Doctor', views.Doctor_view, name='reqAppt_Doctor'),
    path('Patient', views.Patient_view, name='reqAppt_Patient'),
    path('Admin', views.Admin_view, name='reqAppt_Admin'),
    path('Appointment', views.Appointment_view, name='reqAppt_Appointment'),
    path('Pending', views.Pending, name='reqAppt_Pending'),
    path('delete/<id>', views.Destroy, name='reqAppt_delete'),
]
