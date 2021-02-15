from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from ReqAppt import models
from ReqAppt.forms import *
from ReqAppt.models import ApptTable

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
User = get_user_model()

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

def Appointment_view(request):
    if request.method == 'POST':
        form = ApptRequestForm(request.POST)
        if not form.is_valid():
            #Invalid, return 400
            return HttpResponseBadRequest()
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
            ApptTable.objects.create(
                **form.cleaned_data, meetingDate=meetingDate
            )
            return render(request, 'ReqAppt/Pending.html')

    else:
        # if request.user.user_type == 1:
        #     form = ApptRequestForm()
        #     return render(request,'ReqAppt/appointment.html', {"form": form})
        # elif request.user.user_type == 2:
        #     form = ApptRequestFormDoc()
        #     return render(request,'ReqAppt/appointment_doctor.html', {"form": form})
        # elif request.user.user_type == 3:
        #     form = ApptRequestFormPatient()
        #     return render(request,'ReqAppt/appointment_patient.html', {"form": form})
        #form = ApptRequestFormDoc()
        form = ApptRequestForm()
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
    return render(request,'ReqAppt/Patient_view.html',{'ApptTable':x})

def approve(request,id):
    appointment=ApptTable.objects.get(apptId=id)
    appointment.status=True
    appointment.save()
    return redirect("reqAppt_Doctor")

def Destroy(request, id):
    appointment = ApptTable.objects.get(apptId=id)
    if request.method == 'POST':
	    appointment.delete()
	    return redirect("reqAppt_Doctor")
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






# def Appointment_view(request):
#
#     if request.method == 'POST':
#         form = ApptRequestForm(request.POST)
#         if not form.is_valid():
#             #Invalid, return 400
#             return HttpResponseBadRequest()
#         else:
#             # Valid, persist in db
#             ApptTable.objects.create(
#                 **form.cleaned_data
#             )
#             return render(request, 'ReqAppt/Pending.html')
#
#     else:
#         form = ApptRequestForm()
#         return render(request,'ReqAppt/appointment.html', {"form": form})