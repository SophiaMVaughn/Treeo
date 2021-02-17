from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from ReqAppt.forms import ApptRequestForm
from ReqAppt.models import ApptTable



def home(request):
    
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

    cal = Calendar(dday.year, dday.month)
    html_cal = cal.formatTheMonth(withyear=True)
    context = {}
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = previous_month(dday)
    context['next_month'] = next_month(dday)
    return render(request,'ReqAppt/apt_home.html', context)


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




