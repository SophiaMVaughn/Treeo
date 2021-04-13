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
import datetime
import calendar
from users_acc.models import *
from django.db.models import Q

@login_required
def patientlog(request):
    if request.method =='POST':
        if request.user.user_type==3:
            form = PatientLogForm(request.POST)
            if form.is_valid():
                print("flag")
                saverecord = PatientLog()
                saverecord.patient = request.user.patient
                saverecord.calories = form.cleaned_data.get('calories')
                saverecord.water = form.cleaned_data.get('water')
                saverecord.mood = form.cleaned_data.get('mood')
                saverecord.sleep = form.cleaned_data.get('sleep')
                saverecord.save()
                saverecord.date = datetime.datetime.today()
                saverecord.save()
                #when this is saved tis saved as monday rathe than sun
                return render(request, 'patient_log/patientLog_submit.html', {"form": saverecord})
            else:
                return render(request, 'patient_log/patientLog.html', {"form": PatientLogForm(),'formerrors': form})
        elif request.user.user_type==2:
            return redirect('log-chart', request.POST['patient'])
        elif request.user.user_type == 1:
            return redirect('log-chart', request.POST['patient'])
    else:
        if request.user.user_type==3:
            today = datetime.datetime.today().date()
            if PatientLog.objects.filter(patient=request.user.patient.id).filter(date__date=today).exists():
                saverecord = PatientLog.objects.get(Q(patient=request.user.patient.id) & Q(date__date=today))
                return redirect('edit_log',saverecord.id)
            else:
                #link to chart on the page
                return render(request, 'patient_log/patientLog.html', {"form": PatientLogForm()})
        elif request.user.user_type==2:
            context={}
            master_list=[]
            try:
                if request.user.provider.Provider_type ==1:
                    q = Patient.objects.filter(doc_p=request.user.provider)
                elif request.user.provider.Provider_type ==2:
                    q = Patient.objects.filter(doc_d=request.user.provider)
                elif request.user.provider.Provider_type ==3:
                    q = Patient.objects.filter(doc_c=request.user.provider)
                # g=PatientLog.objects.filter(patient__in=q)
                for i in q:
                    if PatientLog.objects.filter(patient=i).exists():
                        master_list.append(PatientLog.objects.filter(patient=i).order_by('date').first())
                    else:
                        pass
            except Exception as e:
                print(e)
            context['patients']=master_list
            print(master_list)
            return render(request, 'patient_log/patientLog.html', context)
        elif request.user.user_type == 1:
            #reject admins
            return redirect('home')

def edit_log(request,id):
    temp = PatientLog.objects.get(id=id)
    form = PatientLogForm()
    if request.method =='POST':
        print("edit_log")
        form = PatientLogForm(request.POST)
        if form.is_valid():
            temp.calories = form.cleaned_data.get('calories')
            temp.water = form.cleaned_data.get('water')
            temp.mood = form.cleaned_data.get('mood')
            temp.sleep = form.cleaned_data.get('sleep')
            temp.save()
            #message.success(request,'')
            #redirects to self
            return render(request, 'patient_log/patientLog_submit.html')
        else:
            form2=PatientLogForm()
        return render(request,'patient_log/editLog.html', {'edit_log': form2,'formerrors': form, 'form':temp})
    else:
        return render(request, 'patient_log/editLog.html', {'edit_log': form, 'form': temp})

def line_chart_Year(id):
    labels = ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"]
    data = []
    data2 = []
    data3 = []
    data4 = []
    #for current year loop through the months and append the average to list make 0 jan 2 feb ect
    cur_date = datetime.datetime.today()

    #second for loop for the years in the PatientLog
    for i in range(1, 13):
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('calories')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data += temp
        else:
            data += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('water')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data2 += temp
        else:
            data2 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('sleep')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data3 += temp
        else:
            data3 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__year=cur_date.year).filter(date__month=i).aggregate(Sum('mood')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data4 += temp
        else:
            data4 += ['NaN']
    #print(data, data2, data3, data4)
    timeframe=cur_date.strftime("%Y")
    # print(timeframe)
    return {
        'labels': labels,
        'Calories': data,
        'Water': data2,
        'Sleep': data3,
        'Mood': data4,
        'timeframe':timeframe}

def line_chart_Month(id):
    #???? declare as empty and populate with the days as it loops
    labels = []
    data = []
    data2 = []
    data3 = []
    data4 = []
    #for current week
    cur_date = datetime.datetime.today()
    num_days = calendar.monthrange(cur_date.year, cur_date.month)[1]
    # print(num_days)
    for day in range(1, num_days + 1):
        labels += [str(day)]
        temp = list(PatientLog.objects.filter(patient=id).filter(date__month=cur_date.month).filter(date__day=day).aggregate(Sum('calories')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data += temp
        else:
            data += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__month=cur_date.month).filter(date__day=day).aggregate(Sum('water')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data2 += temp
        else:
            data2 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__month=cur_date.month).filter(date__day=day).aggregate(Sum('sleep')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data3 += temp
        else:
            data3 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__month=cur_date.month).filter(date__day=day).aggregate(Sum('mood')).values())
        if None not in temp:
            temp[0]=float(temp[0])
            data4 += temp
        else:
            data4 += ['NaN']
    #print(data,data2,data3,data4)
    timeframe=cur_date.strftime("%B")
    # print(timeframe)
    return {
        'labels': labels,
        'Calories': data,
        'Water': data2,
        'Sleep': data3,
        'Mood': data4,
        'timeframe':timeframe
    }
def line_chart_Week(id):
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = []
    data2 = []
    data3 = []
    data4 = []
    #for current week
    cur_date = datetime.datetime.today()
    weekday = cur_date.weekday()
    dates = []
    date = cur_date - datetime.timedelta(days=weekday)

    for i in range(7):
        dates.append(date + datetime.timedelta(days=i))
    for i in dates:
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('calories')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data += temp
        else:
            data += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('water')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data2 += temp
        else:
            data2 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('sleep')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data3 += temp
        else:
            data3 += ['NaN']
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('mood')).values())
        if None not in temp:
            temp[0]=float(temp[0])
            data4 += temp
        else:
            data4 += ['NaN']
    #print(data,data2,data3,data4)
    timeframe=dates[0].strftime("%B %d-") + dates[6].strftime("%d, %Y")
    return {
        'labels': labels,
        'Calories': data,
        'Water': data2,
        'Sleep': data3,
        'Mood': data4,
        'timeframe':timeframe
    }
def render_chart(request, id):
    yearly=line_chart_Year(id)
    monthly=line_chart_Month(id)
    weekly=line_chart_Week(id)
    return render(request, 'patient_log/chart_View.html', {
        'Weekly': weekly,
        'Monthly': monthly,
        'Yearly': yearly,
    })
