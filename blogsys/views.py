from django.shortcuts import render
from django.http import HttpResponseBadRequest
from blogsys.models import PostQ
from .forms import PostQform
from users_acc.models import *





def setter(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)
    if(q==1):
        name[0] = (q[0].user.first_name +" "+ q[0].user.last_name)
    if (q == 2):
        name[1] = (q[1].user.first_name +" "+ q[1].user.last_name)
    if (q == 3):
        name[2] = (q[2].user.first_name +" "+ q[2].user.last_name)
    if (q == 4):
        name[3] = (q[3].user.first_name +" "+ q[3].user.last_name)
    if (q == 5):
        name[4] = (q[4].user.first_name +" "+ q[4].user.last_name)
    if (q == 6):
        name[5] = (q[5].user.first_name +" "+ q[5].user.last_name)
    if (q == 7):
        name[6] = (q[6].user.first_name +" "+ q[6].user.last_name)
    if (q == 8):
        name[7] = (q[7].user.first_name +" "+ q[7].user.last_name)
    if (q == 9):
        name[8] = (q[8].user.first_name +" "+ q[8].user.last_name)
    if (q == 10):
        name[9] = (q[9].user.first_name +" "+ q[9].user.last_name)
    name=[name[0],name[1],name[2],name[3],name[4],name[5],name[6],name[7],name[8],name[9]]
    return(name)
# This First Function is a bit long due to it being called and used for bot patient and provider.
def Health_Coach(request):
    # If patient
    if request.user.user_type == 3:
        x = PostQ.objects.filter( Thereciever= (request.user.patient.user), Thesender=(request.user.patient.doc_c.user))
        if request.method == 'POST':
            form = PostQform(request.POST)

            if form.is_valid():
                save = PostQ()
                save.Message = form.cleaned_data.get('Message')
                save.Thereciever = (request.user.patient.user)
                save.TheActualsender=(request.user.patient.user)
                save.Thesender= (request.user.patient.doc_c.user)
                save.save()
                form = PostQform()

                if request.user.user_type == 3:
                    First = request.user.patient.doc_c.user.first_name
                    Last = request.user.patient.doc_c.user.last_name

                    return render(request, 'blogsys/Health_Coach.html',
                                {"form": form, 'PostQ': x, "First": First, "Last": Last})


                else:
                    return HttpResponseBadRequest()
        else:
            form = PostQform()
            if request.user.user_type == 3:
                if request.user.user_type == 3:
                    First = request.user.patient.doc_c.user.first_name
                    Last = request.user.patient.doc_c.user.last_name

                    return render(request, 'blogsys/Health_Coach.html',
                                {"form": form, 'PostQ': x, "First": First, "Last": Last})

    # If Provider Duplicated to get sender and receiver info

    if request.user.user_type == 2:
        if request.user.provider.Provider_type == 1:
            q = Patient.objects.filter(doc_p=request.user.provider)[0:]
        elif request.user.provider.Provider_type == 2:
            q = Patient.objects.filter(doc_d=request.user.provider)[0:]
        elif request.user.provider.Provider_type == 3:
            q = Patient.objects.filter(doc_c=request.user.provider)[0:]
        if request.method == 'POST':
            form = PostQform(request.POST)

            if form.is_valid():
                save = PostQ()
                save.Message = form.cleaned_data.get('Message')
                save.TheActualsender = (request.user.provider.user)
                save.Thesender = (request.user.provider.user)

                save.Thereciever = (q[0].user)
                save.save()
                form = PostQform()



                if request.user.user_type == 2:
                    if request.user.provider.Provider_type == 1:
                        q = Patient.objects.filter(doc_p=request.user.provider)[0:]
                    elif request.user.provider.Provider_type == 2:
                        q = Patient.objects.filter(doc_d=request.user.provider)[0:]
                    elif request.user.provider.Provider_type == 3:
                        q = Patient.objects.filter(doc_c=request.user.provider)[0:]

                    if len(q) >= 1:
                        name[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = setter(request)
                        x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                        return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
                    else:
                        name[0] = "N/A"
                        return render(request, 'blogsys/noassigned.html',
                                      {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3],
                                       "name5": name[4],
                                       "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                       "name10": name[9]})
                else:
                    return HttpResponseBadRequest()
        else:
            form = PostQform()

            if request.user.user_type == 2:
                if request.user.provider.Provider_type == 1:
                    q = Patient.objects.filter(doc_p=request.user.provider)[0:]
                elif request.user.provider.Provider_type == 2:
                    q = Patient.objects.filter(doc_d=request.user.provider)[0:]
                elif request.user.provider.Provider_type == 3:
                    q = Patient.objects.filter(doc_c=request.user.provider)[0:]

                if len(q) >= 1:
                    x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                    name[0,1,2,3,4,5,6,7,8,9]=setter(request)
                    print(name)
                    return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
                else:
                    name[0] = "N/A"
                    return render(request, 'blogsys/noassigned.html',
                                  {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3],
                                   "name5": name[4],
                                   "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                   "name10": name[9]})

def provider(request):

    x = PostQ.objects.filter(Thereciever=(request.user.patient.user), Thesender= (request.user.patient.doc_p.user))
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save=PostQ()
            save.Message=form.cleaned_data.get('Message')
            save.Thereciever=(request.user.patient.user)
            save.Thesender = (request.user.patient.doc_p.user)
            save.TheActualsender = (request.user.patient.user)
            save.save()
            form = PostQform()
            First = request.user.patient.doc_p.user.first_name
            Last = request.user.patient.doc_p.user.last_name

            return render(request, 'blogsys/provider.html',
                          {"form": form, 'PostQ': x, "First": First, "Last": Last})
        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        First = request.user.patient.doc_p.user.first_name
        Last = request.user.patient.doc_p.user.last_name

        return render(request, 'blogsys/provider.html', {"form": form, 'PostQ': x, "First": First, "Last": Last})



def dietitian(request):
    x = PostQ.objects.filter(Thereciever = (request.user.patient.user),Thesender = (request.user.patient.doc_d.user))

    if request.method =='POST':
        form = PostQform(request.POST)

        if form.is_valid():

            save=PostQ()
            save.Message=form.cleaned_data.get('Message')
            save.Thereciever = (request.user.patient.user)
            save.TheActualsender = (request.user.patient.user)
            save.Thesender = (request.user.patient.doc_d.user)
            save.save()
            form=PostQform()
            First = request.user.patient.doc_d.user.first_name
            Last = request.user.patient.doc_d.user.last_name

            return render(request, 'blogsys/dietitian.html',
                          {"form": form, 'PostQ': x, "First": First, "Last": Last})
        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        First = request.user.patient.doc_d.user.first_name
        Last = request.user.patient.doc_d.user.last_name

        return render(request, 'blogsys/dietitian.html', {"form": form, 'PostQ': x, "First": First, "Last": Last})
def Patient1(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[0:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[0:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[0:]
    if request.method == 'POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thesender = (request.user.provider.user)
            save.TheActualsender = (request.user.provider.user)
            save.Thereciever = (q[0].user)

            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                name[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = setter(request)
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
            else:
                name[0] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = setter(request)
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
        else:
            name[0] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
def Patient2(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[1:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[1:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[1:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
            else:
                name[1] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
        else:
            name[1]="N/A"
            return render(request, 'blogsys/noassigned.html',{"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})


def Patient3(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[2:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[2:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[2:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
            else:
                name[2] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
        else:
            name[2] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient4(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[3:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[3:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[3:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
            else:
                name[3] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0],"name1":name[0],"name2":name[1],"name3":name[2],"name4":name[3],"name5":name[4],"name6":name[5],"name7":name[6],"name8":name[7],"name9":name[8],"name10":name[9]})
        else:
            name[3] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
def Patient5(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[4:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[4:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[4:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0],"name5":name[4]})
            else:
                name[4] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0],"name5":name[4]})
        else:
            name[4] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient6(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[5:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[5:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[5:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0],"name6":name[5]})
            else:
                name[5] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0],"name6":name[5]})
        else:
            name[5] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient7(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[6:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[6:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[6:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0],"name7":name[6]})
            else:
                name[6] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0],"name7":name[6]})
        else:
            name[6] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient8(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[7:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[7:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[7:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.Thereciever = (q[0].user)
            save.TheActualsender = (request.user.provider.user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q":q[0],"name8":name[7]})
            else:
                name[7] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0],"name8":name[7]})
        else:
            name[7] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient9(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[8:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[8:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[8:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.TheActualsender = (request.user.provider.user)
            save.Thereciever = (q[0].user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()

            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0],"name9":name[8]})
            else:
                name[8] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0],"name9":name[8]})
        else:
            name[8] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def Patient10(request):
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[9:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[9:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[9:]
    if request.method =='POST':
        form = PostQform(request.POST)
        if form.is_valid():
            save = PostQ()
            save.TheActualsender = (request.user.provider.user)
            save.Thereciever = (q[0].user)
            save.Thesender = (request.user.provider.user)
            save.Message = form.cleaned_data.get('Message')
            save.save()
            form = PostQform()
            if len(q) >= 1:
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0],"name10":name[9]})
            else:
                name[9] = "N/A"
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0],"name10":name[9]})
        else:
            name[9] = "N/A"
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})

def noassigned(request):
    return render(request, 'blogsys/noassigned.html')



