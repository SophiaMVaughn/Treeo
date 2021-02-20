from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from patient_log.models import PatientLog
from .forms import PatientLogForm, AdminProviderLogForm
from decimal import Decimal
from django.contrib import messages
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from patient_log.models import PatientLog
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
import sched, time
from django.views.generic.edit import UpdateView
from datetime import datetime
from django.db.models import Q

@login_required
def patientlog(request):
    if request.method =='POST':
        if request.user.user_type==3:
            form = PatientLogForm(request.POST)
            if form.is_valid():
                today = datetime.today().date()
                if PatientLog.objects.filter(patient=request.user.patient.id).filter(date__date=today).exists():
                    saverecord=PatientLog.objects.get(Q(patient=request.user.patient.id) & Q(date__date=today))
                    #theoretical error wherein the date time set happens at midnight on the next day
                    saverecord.date = datetime.now()
                else:
                    saverecord = PatientLog()
                saverecord.patient = request.user.patient
                saverecord.calories = form.cleaned_data.get('calories')
                saverecord.water = form.cleaned_data.get('water')
                saverecord.blood = form.cleaned_data.get('blood')
                saverecord.save()
                return render(request, 'patient_log/patientLog_submit.html', {"form": saverecord})
            else:
                return render(request, 'patient_log/patientLog.html', {"form": PatientLogForm()})
        elif request.user.user_type==2:
            return redirect('log-chart', request.POST['patient'])
        elif request.user.user_type == 1:
            return redirect('log-chart', request.POST['patient'])
    else:
        if request.user.user_type==3:
            return render(request, 'patient_log/patientLog.html', {"form": PatientLogForm()})
        elif request.user.user_type==2:
            return render(request, 'patient_log/patientLog.html', {"form": AdminProviderLogForm(instance=request)})
        elif request.user.user_type == 1:
            return render(request, 'patient_log/patientLog.html', {"form": AdminProviderLogForm(instance=request)})



def pie_chart(request,id):
    labels = ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"]
    data = []
    data2 = []
    data3 = []
    #for current year loop through the months and append the average to list make 0 jan 2 feb ect
    cur_date = datetime.today()
    #second for loop for the years in the PatientLog
    for i in range(1, cur_date.month+1):
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('calories')).values())
        if None not in temp:
            data += temp
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('water')).values())
        if None not in temp:
            data2 += temp
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('blood')).values())
        if None not in temp:
            data3 += temp
    print(data,data2, data3)
    for i,val in enumerate(data):
        data[i] = float(val)
    for i,val in enumerate(data2):
        data2[i] = float(val)
    for i,val in enumerate(data3):
        data3[i] = float(val)
    return render(request, 'patient_log/chart_View.html', {
        'labels': labels,
        'data': data,
        'data2': data2,
        'data3': data3,
    })



# def chart(request):
#     return render(request,'patient_log/chart_View.html')
#
# class Circle(BaseLineChartView):
#     slug = None
#     print("2")
#     def get_labels(self):
#         return ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"]
#
#     def get_providers(self):
#         return ["Central", "Eastside", "Westside"]
#
#
#     def get_data(self):
#         aaa = list(PatientLog.objects.filter(patient=id).aggregate(Sum('blood')).values())[0]
#         baa = list(PatientLog.objects.filter(patient=id).aggregate(Sum('calories')).values())[0]
#         caa = list(PatientLog.objects.filter(patient=id).aggregate(Sum('water')).values())[0]
#         print(self.kwargs['slug'])
#         return [[ baa, 2000,1222,1111],
#               [aaa, 2.1],
#                 [caa,1.4]]










