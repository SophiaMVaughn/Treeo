from django.shortcuts import render
from django.http import HttpResponseBadRequest

from ReqAppt import models
from patient_log.models import PatientLog
from .forms import PatientLogForm
from decimal import Decimal
from django.contrib import messages

def patientlog(request):
    #context = {'form':PatientLogForm()}
    if request.method =='POST':
        form = PatientLogForm(request.POST)
        print("1")
        if form.is_valid():
            print("3")
            print(form.cleaned_data.get('calories'))
            saverecord=PatientLog()
            saverecord.calories=form.cleaned_data.get('calories')
            saverecord.water=form.cleaned_data.get('water')
            saverecord.blood=form.cleaned_data.get('blood')
            saverecord.save()
            #messages.success('your data was saved!')
            return render(request, 'patient_log/patientLog.html ')
        else:
            print("2")
            return HttpResponseBadRequest()
    else:
        form = PatientLogForm()
        return render(request, 'patient_log/patientLog.html', {"form": form})


