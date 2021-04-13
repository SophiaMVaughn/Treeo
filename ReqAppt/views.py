#Brandon
#Giorgi
#Allan
import calendar
import json

from django.contrib.sites import requests
import math

from utils.calendar import Calendar
from django.utils.safestring import mark_safe
from ReqAppt import models
from datetime import datetime, date, timedelta
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from ReqAppt import models
from ReqAppt.forms import *
from ReqAppt.models import ApptTable
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .sms import *
from .email import *
from datetime import datetime
import requests
from .tasks import *
from apptArchive.models import ApptArchive
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


User = get_user_model()

def base64_encode(message):
    import base64
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message





	#Author: Giorgi Nozadze
	#This is the second version of full calendar that can be used, based on client's preference


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


	#Author: Giorgi Nozadze
	#This method is responsible for scheduling appointment scheduling, first it checks form validation, 
   	# if valid appointment is scheduled and some of the methods of other features are called, 
   	# line 123 calls mail notification, line 125 calls text message

def create_Appointment(request):
    if request.method == 'POST':
        form = ApptRequestFormPatient(data=request.POST, instance=request.user)
        if not form.is_valid():
            form2 = ApptRequestFormPatient(instance=request.user)
            return render(request, 'ReqAppt/appointment.html', {"form": form2,'formerrors': form})
            #return HttpResponseBadRequest()
        else:

            # Valid, persist in db
            print(request.POST)
            apptDate = request.POST['apptDate']
            apptHour = float(request.POST['apptHour'])
            print(apptDate)
            print(apptHour)
            meetingDate = datetime.datetime.strptime(apptDate, "%m/%d/%Y")
            hour = int(math.floor(apptHour))
            minute = int((apptHour - hour) * 60)
            meetingDate = meetingDate.replace(hour=hour, minute=minute)
            print(meetingDate)
            appointment=ApptTable.objects.create(
                **form.cleaned_data, meetingDate=meetingDate
            )

            # Oath, TODO use JWT if this doesn't work
            scheduled_mail_both_task.delay(appointment.id)
            target_time_print(appointment)
            send_message_task.delay(appointment.id)
            return render(request, 'ReqAppt/Pending.html')


    else:
        form = ApptRequestFormPatient(instance=request.user)
        return render(request,'ReqAppt/appointment.html', {"form": form})
        #provider = form.cleaned_data.get('user_defined_code')


def Doctor_view(request):
    x = ApptTable.objects.filter(provider= request.user.provider.id).order_by('meetingDate')
    pagination = Paginator(x, 5)
    page = request.GET.get('page', 1)
    try:
        pagination = pagination.page(page)
    except PageNotAnInteger:
        pagination = pagination.page(1)
    except EmptyPage:
        pagination = pagination.page(pagination.num_pages)
    # general except 501????
    context = {
        'ApptTable': pagination
    }
    return render(request,'ReqAppt/Doctor_view.html',context)


def Admin_view(request):
    #need to make some search criteria here
    x = ApptTable.objects.all()
    pagination = Paginator(x, 5)
    page = request.GET.get('page', 1)
    try:
        pagination = pagination.page(page)
    except PageNotAnInteger:
        pagination = pagination.page(1)
    except EmptyPage:
        pagination = pagination.page(pagination.num_pages)
    # general except 501????
    context = {
        'ApptTable': pagination
    }
    return render(request, 'ReqAppt/Admin_view.html', context)


def Patient_view(request):
    x = ApptTable.objects.filter(patient=request.user.patient.id).order_by('meetingDate')
    pagination = Paginator(x, 5)
    page = request.GET.get('page', 1)
    try:
        pagination = pagination.page(page)
    except PageNotAnInteger:
        pagination = pagination.page(1)
    except EmptyPage:
        pagination = pagination.page(pagination.num_pages)
    # general except 501????
    context = {
        'ApptTable': pagination
    }
    return render(request,'ReqAppt/Patient_view.html',context)

def approve(request,id):
    appointment=ApptTable.objects.get(id=id)
    #need error handling
    provider_url, patient_url, patient_pwd = generate_zoom(request=1)
    appointment.meeturlprovider=provider_url
    appointment.meeturlpatient=patient_url
    print(appointment.meeturlprovider)
    print(appointment.meeturlpatient)
    #Confirm Appointment
    appointment.status=True
    appointment.save()
    approve_message_task.delay(appointment.id)
    approved_mail_both_task.delay(appointment.id,patient_pwd)
    return redirect("reqAppt_Doctor")

# Delete Appointment
def Destroy(request, id):
    appointment = ApptTable.objects.get(id=id)
    if request.method == 'POST':
        appointment.delete()
        reject_message_task.delay(appointment.id)
        reject_mail_both_task.delay(appointment.id)
        return redirect ("reqAppt_Doctor")
    return render(request,"reqAppt/DeleteConfirm.html")



	#Author: Giorgi Nozadze
	#This method checks for available time slots for the appointments

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
        return appt.meetingDate.hour + (appt.meetingDate.minute * 0.5)

    unavailable_times = {appt_to_time(appt) for appt in appointments}

    # in order to switch time slots from 60 minutes to 30 minutes use line 237 instead of 238
    # second one simply divides h by 2
    # data = [h/2 for h in range(STARTING_HOUR * 2, (ENDING_HOUR + 1) * 2) if h/2 not in unavailable_times]
    data = [h for h in range(STARTING_HOUR , ENDING_HOUR + 1) if h not in unavailable_times]

    # return json response of available time slots
    return JsonResponse(data, safe=False)


#### FULL CALLENDAR

	#Author: Giorgi Nozadze
	#This method displays appointment time bars on the full calendar

def event(request):
    meeting_arr = []
    #if request.GET.get('patient') == "all":
    #    all_meetings = ApptTable.objects.all()
    #else:
    #    all_meetings = ApptTable.objects.filter(event_type__icontains=request.GET.get('event_type'))

    is_patient = [type_name for t, type_name in USER_TYPE_CHOICES if t == request.user.user_type][0] == 'Patient'
    if is_patient:
        all_meetings = ApptTable.objects.filter(patient__user_id=request.user.id).all()
    else:
        all_meetings = ApptTable.objects.filter(provider__user_id=request.user.id).all()

    for i in all_meetings:
        meeting_sub_arr = {}
        user = (i.provider if is_patient else i.patient).user
        meeting_sub_arr['title'] = f"{user.first_name} {user.last_name}"
        start = i.meetingDate.strftime('%Y-%m-%dT%H:%M:%S')
        end = (i.meetingDate + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
        #meetingDate = datetime.strptime(str(i.meetingDate.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        meeting_sub_arr['start'] = start
        meeting_sub_arr['end'] = end
        meeting_arr.append(meeting_sub_arr)
    return HttpResponse(json.dumps(meeting_arr))


	#Author: Giorgi Nozadze
	#This method displays full calendar 

def fullcalendar(request):
    all_meetings = ApptTable.objects.all()
    get_meeting_patients = ApptTable.objects.only('patient')

    # if filters applied then get parameter and filter based on condition else return object
    print(request.method)

    context = {
        "meeting":all_meetings,
        "get_meeting_patient":get_meeting_patients,
    }
    return render(request,'ReqAppt/fullcalendar.html',context)

# def archive_apt(request,id):
#     #try error handling
#     appointment = ApptTable.objects.get(id=id)
#     try:
#         archiveAppt = ApptArchive.objects.create()
#         archiveAppt.meetingDate = appointment.meetingDate
#         archiveAppt.provider = appointment.provider
#         archiveAppt.patient = appointment.patient
#         archiveAppt.save()
#         appointment.delete()
#         return render(request,"reqAppt/appointment.html")
#     except Exception as e:
#         print(e)
#         return render(request,"reqAppt/appointment.html")


#     is_patient = [type_name for t, type_name in USER_TYPE_CHOICES if t == request.user.user_type][0] == 'Patient'
#     if is_patient:
#         all_meetings = ApptTable.objects.filter(patient__user_id=request.user.id).all()
#     else:
#         all_meetings = ApptTable.objects.filter(provider__user_id=request.user.id).all()

#     for i in all_meetings:
#         meeting_sub_arr = {}
#         user = (i.provider if is_patient else i.patient).user
#         meeting_sub_arr['title'] = f"{user.first_name} {user.last_name}"
#         start = i.meetingDate.strftime('%Y-%m-%dT%H:%M:%S')
#         end = (i.meetingDate + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
#         #meetingDate = datetime.strptime(str(i.meetingDate.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
#         meeting_sub_arr['start'] = start
#         meeting_sub_arr['end'] = end
#         meeting_arr.append(meeting_sub_arr)
#     return HttpResponse(json.dumps(meeting_arr))

# def archive_apt(id):
#     appointment = ApptTable.objects.get(id=id)
#     try:
#         archiveAppt = ApptArchive.objects.create()
#         archiveAppt.meetingDate = appointment.meetingDate
#         archiveAppt.provider = appointment.provider
#         archiveAppt.patient = appointment.patient
#         archiveAppt.save()
#         appointment.delete()
#     except Exception as e:
#         print(e)


