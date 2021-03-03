
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='reqAppt'),
    path('reqAppt_calendar', views.reqAppt_calendar, name='reqAppt_calendar'),
    path('Doctor', views.Doctor_view, name='reqAppt_Doctor'),
    path('Patient', views.Patient_view, name='reqAppt_Patient'),
    path('Admin', views.Admin_view, name='reqAppt_Admin'),
    path('Appointment', views.create_Appointment, name='create_Appointment'),
    path('availability/provider/<int:id>/date/<str:date_str>', views.Doctor_avail_view),
    path('Pending', views.Pending, name='reqAppt_Pending'),
    path('delete/<id>', views.Destroy, name='reqAppt_delete'),
    path('approveappt/<id>', views.approve, name='approve_appt'),
    path('archive/<id>', views.archive_apt, name='archive'),
]