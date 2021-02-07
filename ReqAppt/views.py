from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from ReqAppt.forms import ApptRequestForm
from ReqAppt.models import ApptTable


def home(request):
    return render(request,'ReqAppt/home.html')

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



