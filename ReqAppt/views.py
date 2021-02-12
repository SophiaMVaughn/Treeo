from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from ReqAppt.forms import ApptRequestForm
from ReqAppt.models import ApptTable


def home(request):
    return render(request,'ReqAppt/apt_home.html')

def Pending(request):
    return render(request,'ReqAppt/Pending.html')

def Doctor_view(request):
    x = ApptTable.objects.all()
    return render(request,'ReqAppt/Doctor_view.html',{'ApptTable':x})


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
        form = ApptRequestForm()
        return render(request,'ReqAppt/appointment.html', {"form": form})

        provider = form.cleaned_data.get('user_defined_code')


def Admin_view(request):
    x = ApptTable.objects.all()
    return render(request, 'ReqAppt/Admin_view.html', {'ApptTable': x})


def Patient_view(request):
    x = ApptTable.objects.all()
    return render(request,'ReqAppt/Patient_view.html',{'ApptTable':x})


def Destroy(request, id):
    appointment = ApptTable.objects.get(apptId=id)
    appointment.delete()
    return redirect("reqAppt_Doctor")




