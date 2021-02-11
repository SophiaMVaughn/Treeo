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
            ApptTable.objects.create(
                **form.cleaned_data
            )
            return render(request, 'ReqAppt/Pending.html')

    else:
        form = ApptRequestForm()
        return render(request,'ReqAppt/appointment.html', {"form": form})

def Admin_view(request):
    x = ApptTable.objects.all()
    return render(request, 'ReqAppt/Admin_view.html', {'ApptTable': x})


def Patient_view(request):
    x = ApptTable.objects.all()
    return render(request,'ReqAppt/Patient_view.html',{'ApptTable':x})


def Destroy(request, id):
    appointment = ApptTable.objects.get(apptId=id)
    if request.method == 'POST':
	    appointment.delete()
	    return redirect("reqAppt_Doctor")
    return render(request,"reqAppt/DeleteConfirm.html")


def approve(request,id):
    appointment=ApptTable.objects.get(apptId=id)
    appointment.status=True
    appointment.save()
    return redirect("reqAppt_Doctor")


