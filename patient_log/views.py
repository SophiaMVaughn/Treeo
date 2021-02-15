from django.shortcuts import render
from django.http import HttpResponseBadRequest
from patient_log.models import PatientLog
from .forms import PatientLogForm
from decimal import Decimal
from django.contrib import messages
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from patient_log.models import PatientLog
from django.db.models import Sum
import sched, time
from django.views.generic.edit import UpdateView

aaa = list(PatientLog.objects.aggregate(Sum('blood')).values())[0]
baa = list(PatientLog.objects.aggregate(Sum('calories')).values())[0]
caa = list(PatientLog.objects.aggregate(Sum('water')).values())[0]


def patientlog(request):
    #context = {'form':PatientLogForm()}
    if request.method =='POST':
        form = PatientLogForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data.get('calories'))
            saverecord=PatientLog()
            saverecord.calories=form.cleaned_data.get('calories')
            saverecord.water=form.cleaned_data.get('water')
            saverecord.blood=form.cleaned_data.get('blood')
            saverecord.save()

            #messages.success('your data was saved!')

            return render(request, 'patient_log/patientLog_submit.html ', {"form":saverecord})

        else:

            return HttpResponseBadRequest()
    else:
        form = PatientLogForm()
        return render(request, 'patient_log/patientLog.html', {"form": form})



def chart(request):
    return render(request,'patient_log/chart_View.html')





class Circle(BaseLineChartView):

    print("2")
    def get_labels(self):
        return ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"]

    def get_providers(self):
        return ["Central", "Eastside", "Westside"]


    def get_data(self):
        aaa = list(PatientLog.objects.aggregate(Sum('blood')).values())[0]
        baa = list(PatientLog.objects.aggregate(Sum('calories')).values())[0]
        caa = list(PatientLog.objects.aggregate(Sum('water')).values())[0]
        return [[ baa, 2000,1222,1111],
              [aaa, 2.1],
                [caa,1.4]]




chart2 = TemplateView.as_view(template_name='chart2.html')
chart_json = Circle.as_view()





