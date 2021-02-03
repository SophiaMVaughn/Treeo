from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,'ReqAppt/home.html')

def Doctor_view(request):
    return render(request,'ReqAppt/Doctor_view.html')

def Patient_view(request):
    return render(request,'ReqAppt/Patient_view.html')

def Admin_view(request):
    return render(request,'ReqAppt/Admin_view.html')
