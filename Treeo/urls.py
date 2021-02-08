from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ReqAppt.urls')),
    path('patientLog/', include('patient_log.urls')),
]