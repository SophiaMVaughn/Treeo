from django.urls import path
from . import views

# from .views import *

urlpatterns = [
    path('', views.patientlog, name='patientlog'),
    # path('Chart', views.chart, name='seechart'),
    # path('charts', Circle.as_view(), name='chart_json'),
    path('calories/<id>', views.Calories, name='calories'),
    path('log-chart/<id>', views.line_chart_Week, name='log-chart'),
    path('log-chart1/<id>', views.Mood, name='mood'),
    path('log-chart2/<id>', views.Sleep, name='sleep'),
    path('log-chart3/<id>', views.Water, name='water'),
    path('edit_log/<id>', views.edit_log, name='edit_log'),
]
