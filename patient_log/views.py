from django.shortcuts import render
from django.http import HttpResponse

def patientLog(request):
    return render(request,'patient_log/patientLog.html ')
