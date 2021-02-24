import calendar


from utils.calendar import Calendar
from django.utils.safestring import mark_safe
from ReqAppt import models
from datetime import datetime, date, timedelta
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from ReqAppt import models
from ReqAppt.forms import *
from ReqAppt.models import ApptTable
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .sms import *


User = get_user_model()



def reqAppt_calendar(request):
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     d = get_date(self.request.GET.get('month', None))
    #     cal = Calendar(d.year, d.month)

    def previous_month(dday):
        firstDayofMonth = dday.replace(day=1)
        previous_month = firstDayofMonth - timedelta(days=1)
        calMonth = 'month=' + str(previous_month.year) + '-' + str(previous_month.month)
        return calMonth

    def next_month(dday):
        days_in_month = calendar.monthrange(dday.year, dday.month)[1]
        last = dday.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month

    #placeholder for a year and a month
    if 'month' in request.GET:
        year, month = request.GET['month'].split("-")
        year, month = int(year), int(month)
        dday = date(year=year, month=month, day=1)
    else:
        dday = datetime.now()

    cal = Calendar(dday.year, dday.month, request)
    html_cal = cal.formatTheMonth(withyear=True)
    context = {}
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = previous_month(dday)
    context['next_month'] = next_month(dday)
    return render(request,'ReqAppt/apt_calendar.html', context)

@login_required
def home(request):
    if request.user.user_type==1:
        return Admin_view(request)
    elif request.user.user_type == 2:
        return Doctor_view(request)
    elif request.user.user_type == 3:
        return Patient_view(request)
    else:
        return render(request,'ReqAppt/apt_home.html')

def Pending(request):
    return render(request,'ReqAppt/Pending.html')


#zoom account required decorator
def create_Appointment(request):
    if request.method == 'POST':
        form = ApptRequestFormPatient(data=request.POST, instance=request.user)
        if not form.is_valid():
            form = ApptRequestFormPatient(instance=request.user)
            #return some error message
            return render(request, 'ReqAppt/appointment.html', {"form": form})
            #return HttpResponseBadRequest()
        else:
            # Valid, persist in db
            print(request.POST)
            apptDate = request.POST['apptDate']
            apptHour = request.POST['apptHour']
            print(apptDate)
            print(apptHour)
            meetingDate = datetime.strptime(apptDate, "%m/%d/%Y")
            meetingDate = meetingDate.replace(hour=int(apptHour))
            print(meetingDate)
            #call zoom api make meeting and get the url for it
            # ApptTable.objects.create(
            #     **form.cleaned_data, meetingDate=meetingDate meeturl=zoom url
            # )
            g=ApptTable.objects.create(
                **form.cleaned_data, meetingDate=meetingDate
            )
            send_message(apptDate, apptHour)
            # who are you sending this too? patient
            scheduled_mail_both(g)

            return render(request, 'ReqAppt/Pending.html')

    else:
        form = ApptRequestFormPatient(instance=request.user)
        return render(request,'ReqAppt/appointment.html', {"form": form})
        #provider = form.cleaned_data.get('user_defined_code')



def Doctor_view(request):
    x = ApptTable.objects.filter(provider= request.user.provider.id).order_by('meetingDate')
    return render(request,'ReqAppt/Doctor_view.html',{'ApptTable':x})


def Admin_view(request):
    #need to make some search criteria here
    x = ApptTable.objects.all()
    return render(request, 'ReqAppt/Admin_view.html', {'ApptTable': x})


def Patient_view(request):
    x = ApptTable.objects.filter(patient=request.user.patient.id).order_by('meetingDate')
    for i in x:
        print(i.meetingDate)
    return render(request,'ReqAppt/Patient_view.html',{'ApptTable':x})

def approve(request,id):
    appointment=ApptTable.objects.get(apptId=id)
    appointment.status=True
    appointment.save()
    approve_message()
    approved_mail_both(appointment)
    return redirect("reqAppt_Doctor")

def Destroy(request, id):
    appointment = ApptTable.objects.get(apptId=id)
    if request.method == 'POST':


        appointment.delete()
        reject_message()
        delete_mail_both(appointment)
        return redirect ("reqAppt_Doctor")
    return render(request,"reqAppt/DeleteConfirm.html")

STARTING_HOUR = 8
ENDING_HOUR = 16
def Doctor_avail_view(request, id, date_str):
    # parse datetime
    # query appointments for id(provider) on date
    # filter for available hour slots from 8-4 , return json list
    month, day, year = date_str.split('-')
    appointments = ApptTable.objects.filter(
        provider_id=id,
        meetingDate__year=str(year),
        meetingDate__month=str(month),
        meetingDate__day=str(day),
    ).all()

    def appt_to_time(appt: ApptTable):
        return appt.meetingDate.hour

    unavailable_times = {appt_to_time(appt) for appt in appointments}

    data = [h for h in range(STARTING_HOUR, ENDING_HOUR+1) if h not in unavailable_times]

    return JsonResponse(data, safe=False)






