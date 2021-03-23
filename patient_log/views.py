from django.shortcuts import render, redirect
from .forms import PatientLogForm, AdminProviderLogForm
from patient_log.models import PatientLog
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.db.models import Q

@login_required
def patientlog(request):
    if request.method =='POST':
        if request.user.user_type==3:
            form = PatientLogForm(request.POST)
            if form.is_valid():
                saverecord = PatientLog()
                saverecord.patient = request.user.patient
                saverecord.calories = form.cleaned_data.get('calories')
                saverecord.water = form.cleaned_data.get('water')
                saverecord.mood = form.cleaned_data.get('mood')
                saverecord.sleep = form.cleaned_data.get('sleep')
                saverecord.save()
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
            return render(request, 'patient_log/patientLog.html', {"form": AdminProviderLogForm(instance=request)})
        elif request.user.user_type == 1:
            return render(request, 'patient_log/patientLog.html', {"form": AdminProviderLogForm(instance=request)})

def edit_log(request,id):
    temp = PatientLog.objects.get(id=id)
    form = PatientLogForm()
    if request.method =='POST':
        print("test")
        form = PatientLogForm(request.POST)
        if form.is_valid():
            temp.calories = form.cleaned_data.get('calories')
            temp.water = form.cleaned_data.get('water')
            temp.mood = form.cleaned_data.get('mood')
            temp.sleep = form.cleaned_data.get('sleep')
            temp.save()
            #message.success(request,'')
            #redirects to self
            return render(request, 'patient_log/patientLog_submit.html', {"form": temp})
        else:
            form2=PatientLogForm()
        return render(request,'patient_log/editLog.html', {'edit_log': form2,'formerrors': form})
    else:
        return render(request, 'patient_log/editLog.html', {'edit_log': form})

def line_chart_Year(request,id):
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
    print(data, data2, data3, data4)
    return render(request, 'patient_log/chart_View.html', {
        'labels': labels,
        'data': data,
        'data2': data2,
        'data3': data3,
        'data4': data4,
    })




def Calories(request,id):
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = []
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
    return render(request, 'patient_log/calories.html', {
        'labels': labels,
        'data': data,
    })


def Water(request,id):
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data2 = []
    #for current week
    cur_date = datetime.datetime.today()
    weekday = cur_date.weekday()
    dates = []
    date = cur_date - datetime.timedelta(days=weekday)
    for i in range(7):
        dates.append(date + datetime.timedelta(days=i))
    for i in dates:
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('water')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data2 += temp
        else:
            data2 += ['NaN']

    return render(request, 'patient_log/water.html', {
        'labels': labels,
        'data2': data2,
    })



def Mood(request,id):
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data4 = []
    #for current week
    cur_date = datetime.datetime.today()
    weekday = cur_date.weekday()
    dates = []
    date = cur_date - datetime.timedelta(days=weekday)
    for i in range(7):
        dates.append(date + datetime.timedelta(days=i))
    for i in dates:
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('mood')).values())
        if None not in temp:
            temp[0]=float(temp[0])
            data4 += temp
        else:
            data4 += ['NaN']
    return render(request, 'patient_log/mood.html', {
        'labels': labels,
        'data4': data4,
    })

def Sleep(request,id):
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data3 = []
    #for current week
    cur_date = datetime.datetime.today()
    weekday = cur_date.weekday()
    dates = []
    date = cur_date - datetime.timedelta(days=weekday)
    for i in range(7):
        dates.append(date + datetime.timedelta(days=i))
    for i in dates:
        temp = list(PatientLog.objects.filter(patient=id).filter(date__date=i).aggregate(Sum('sleep')).values())
        if None not in temp:
            temp[0] = float(temp[0])
            data3 += temp
        else:
            data3 += ['NaN']
    return render(request, 'patient_log/sleep.html', {
        'labels': labels,
        'data3': data3,
    })

def line_chart_Week(request,id):
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
    print(data,data2,data3,data4)
    print(data, data2, data3, data4)
    return render(request, 'patient_log/chart_View.html', {
        'labels': labels,
        'data': data,
        'data2': data2,
        'data3': data3,
        'data4': data4,
    })



