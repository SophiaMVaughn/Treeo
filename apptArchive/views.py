from django.shortcuts import render, redirect
from apptArchive.models import ApptArchive
from apptArchive.forms import NotesForm

def view_archived_appointments(request):
    # query appointment table or notes after they select a n appointment request.user
    if request.user.user_type == 3:
        apptArchive=ApptArchive.objects.filter( patient=request.user.patient).order_by('meetingDate')
        return render(request, 'apptArchive/apptArchive.html', {'apptArchive': apptArchive})
    elif request.user.user_type == 2:
        apptArchive = ApptArchive.objects.filter(provider=request.user.provider).order_by('meetingDate')
        return render(request, 'apptArchive/apptArchive.html', {'apptArchive': apptArchive})
    else:
        redirect('home')

def view_archived_appointment(request,id):
    # the view for the one appointment and all of the notes on it
    if request.user.user_type == 3:
        apptArchive=ApptArchive.objects.filter( patient=request.user.patient).order_by('meetingDate')
        return render(request, 'apptArchive/apptArchive.html', {'apptArchive': apptArchive})
    elif request.user.user_type == 2:
        apptArchive = ApptArchive.objects.filter(provider=request.user.provider).order_by('meetingDate')
        return render(request, 'apptArchive/apptArchive.html', {'apptArchive': apptArchive})
    else:
        redirect('home')

# def create_note(request, id):
#     if request.method =="POST":
#         form = NotesForm(request.POST)
#         if form.is_valid():
#             form.save()
#             redirect('notes view??')
#         else:
#             form2 = NotesForm()
#             return render(request,'patient_log/notes.html', {'form': form2,'formerrors': form})
#     else:
#         form = NotesForm()
#         return render(request, 'patient_log/notes.html', {'form': NotesForm(), 'formerrors': form})