from django.shortcuts import render, redirect
from apptArchive.models import ApptArchive, Notes
from apptArchive.forms import NotesForm

def view_all_archived_appointments(request):
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
    try:
        apptArchive = ApptArchive.objects.get(id=id)
        notes = Notes.objects.filter(apptId=id)
    except:
        # 404 instead??
        redirect('home')
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            Notes.objects.create(apptId=apptArchive, notes=form.cleaned_data.get('notes'))
            notes = Notes.objects.filter(apptId=id)
            return render(request, 'apptArchive/notes.html', {'Archivedappt': apptArchive,'aptnotes': notes, "form": NotesForm()})
    else:
        return render(request, 'apptArchive/notes.html', {'Archivedappt': apptArchive,'aptnotes': notes, "form": NotesForm()})
# def create_note(request, id):
#    if request.user.user_type == 2:
#       if request.method =="POST":
#            form = NotesForm(request.POST)
#            if form.is_valid():
#                form.save()
#                return render(request, 'notes.html', {"form": NotesForm()})
#        else:
#            return render(request, 'notes.html', {"form": NotesForm()})