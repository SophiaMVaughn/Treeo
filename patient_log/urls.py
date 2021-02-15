from django.urls import path
from . import views
from .views import chart2, chart_json

urlpatterns = [
    path('', views.patientlog, name='patientlog'),
    path('Chart', views.chart, name='seechart'),
  path('chart2', chart2, name='chart2'),
  path('charts', chart_json, name='chart_json'),
]