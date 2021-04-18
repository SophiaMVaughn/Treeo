#ALLAN IMSEIS
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from blogsys.models import PostQ
from .forms import PostQform
from users_acc.models import *

#Allan 
#Provider type determined by number
#Patients names stored in list
def setter(request):
    name = []
    name.clear()
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)
        for i in q:
            name.append(i.user.first_name + " " + i.user.last_name)
            j = len(name)
    if request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)
        for i in q:
            name.append(i.user.first_name + " " + i.user.last_name)
            j = len(name)
    if request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)
        for i in q:
            name.append(i.user.first_name + " " + i.user.last_name)
            j = len(name)
    while (len(name) != 10):
        name.append("No Patient Assigned")
    return name


# This First Function is a bit long due to it being called and used for both patient 1 and Health Coach depending on user type.
# First HTML called takes user to this function and locates if statement based on user type. After that the user will only see that content linked to that html.
def Health_Coach(request):
    # If patient
    try:
        if request.user.user_type == 3:
            # For user.patient.doc_c (Health Coach)
            #Takes in message from forms
            #Sent to database
            x = PostQ.objects.filter(Thereciever=(
                request.user.patient.user), Thesender=(request.user.patient.doc_c.user))
            if request.method == 'POST':
                form = PostQform(request.POST)

                if form.is_valid():
                    save = PostQ()
                    save.Message = form.cleaned_data.get('Message')
                    #Stores The number of actual sender and receiver in database
                    save.Thereciever = (request.user.patient.user)
                    save.TheActualsender = (request.user.patient.user)
                    save.Thesender = (request.user.patient.doc_c.user)
                    save.save()
                    form = PostQform()
                    #Takes current patients Health Coach Name
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
                        #Content sent to html
                        return render(request, 'blogsys/Health_Coach.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
    except AttributeError:
        #If no provider assigned return this html
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')

    if request.user.user_type == 2:
        # If provider
        #Finds what provider based on number
        #Takes first patient assigned to said provider [0:]
        if request.user.provider.Provider_type == 1:
            q = Patient.objects.filter(doc_p=request.user.provider)[0:]
        elif request.user.provider.Provider_type == 2:
            q = Patient.objects.filter(doc_d=request.user.provider)[0:]
        elif request.user.provider.Provider_type == 3:
            q = Patient.objects.filter(doc_c=request.user.provider)[0:]
        if request.method == 'POST':
            form = PostQform(request.POST)
            #Form content sent to database
            if form.is_valid():
                save = PostQ()
                #Stores The number of actual sender and receiver in database
                save.Message = form.cleaned_data.get('Message')
                save.TheActualsender = (request.user.provider.user)
                save.Thesender = (request.user.provider.user)

                save.Thereciever = (q[0].user)
                save.save()
                form = PostQform()

                if request.user.user_type == 2:
                    if request.user.provider.Provider_type == 1:
                        q = Patient.objects.filter(
                            doc_p=request.user.provider)[0:]
                    elif request.user.provider.Provider_type == 2:
                        q = Patient.objects.filter(
                            doc_d=request.user.provider)[0:]
                    elif request.user.provider.Provider_type == 3:
                        q = Patient.objects.filter(
                            doc_c=request.user.provider)[0:]

                    if len(q) >= 1:
                        name = setter(request)
                        x = PostQ.objects.filter(Thesender=(
                            #names of all patients sent to HTML from above setter
                            #Content sent to html
                            request.user.provider.user), Thereciever=(q[0].user))
                        return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                         "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                         "name10": name[9]})
                    else:
                        name = setter(request)
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
                    name = setter(request)
                    x = PostQ.objects.filter(Thesender=(
                        request.user.provider.user), Thereciever=(q[0].user))
                    return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                     "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                     "name10": name[9]})

                else:
                    name = setter(request)
                    #No patient assigned return this HTML
                    return render(request, 'blogsys/noassigned.html',
                                  {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3],
                                   "name5": name[4],
                                   "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                   "name10": name[9]})


def provider(request):
    #If patient
    #Same as description above but for provider patient.doc_p
    try:
        if request.user.user_type == 3:
            x = PostQ.objects.filter(Thereciever=(request.user.patient.user),
                                     Thesender=(request.user.patient.doc_p.user))
            if request.method == 'POST':
                form = PostQform(request.POST)

                if form.is_valid():
                    save = PostQ()
                    save.Message = form.cleaned_data.get('Message')
                    save.Thereciever = (request.user.patient.user)
                    save.TheActualsender = (request.user.patient.user)
                    save.Thesender = (request.user.patient.doc_p.user)
                    save.save()
                    form = PostQform()

                    if request.user.user_type == 3:
                        First = request.user.patient.doc_p.user.first_name
                        Last = request.user.patient.doc_p.user.last_name

                        return render(request, 'blogsys/provider.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})

                    else:
                        return HttpResponseBadRequest()
            else:
                form = PostQform()
                if request.user.user_type == 3:
                    if request.user.user_type == 3:
                        First = request.user.patient.doc_p.user.first_name
                        Last = request.user.patient.doc_p.user.last_name

                        return render(request, 'blogsys/provider.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
    except AttributeError:
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')

        return render(request, 'blogsys/provider.html',
                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
    except AttributeError:
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')


def dietitian(request):
    #If Patient
    #Same as description above but for dietitian patient.doc_d
    try:
        if request.user.user_type == 3:
            x = PostQ.objects.filter(Thereciever=(request.user.patient.user),
                                     Thesender=(request.user.patient.doc_d.user))
            if request.method == 'POST':
                form = PostQform(request.POST)

                if form.is_valid():
                    save = PostQ()
                    save.Message = form.cleaned_data.get('Message')
                    save.Thereciever = (request.user.patient.user)
                    save.TheActualsender = (request.user.patient.user)
                    save.Thesender = (request.user.patient.doc_d.user)
                    save.save()
                    form = PostQform()

                    if request.user.user_type == 3:
                        First = request.user.patient.doc_d.user.first_name
                        Last = request.user.patient.doc_d.user.last_name

                        return render(request, 'blogsys/dietitian.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})

                    else:
                        return HttpResponseBadRequest()
            else:
                form = PostQform()
                if request.user.user_type == 3:
                    if request.user.user_type == 3:
                        First = request.user.patient.doc_d.user.first_name
                        Last = request.user.patient.doc_d.user.last_name

                        return render(request, 'blogsys/dietitian.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
    except AttributeError:
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')


def Patient1(request):
    #If Provider
    #Same as function above Patient number 1 [0:]
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient2(request):
    #If Provider
    #Same as function above Patient number 2 [1:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[1:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[1:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[1:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient3(request):
    #If Provider
    #Same as function above Patient number 3 [2:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[2:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[2:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[2:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient4(request):
    #If Provider
    #Same as function above Patient number 4 [3:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[3:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[3:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[3:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient5(request):
    #If Provider
    #Same as function above Patient number 5 [4:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[4:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[4:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[4:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient6(request):
    #If Provider
    #Same as function above Patient number 6 [5:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[5:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[5:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[5:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient7(request):
    #If Provider
    #Same as function above Patient number 7 [6:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[6:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[6:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[6:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient8(request):
    #If Provider
    #Same as function above Patient number 8 [7:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[7:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[7:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[7:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient9(request):
    #If Provider
    #Same as function above Patient number 9 [8:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[8:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[8:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[8:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def Patient10(request):
    #If Provider
    #Same as function above Patient number 10 [9:]
    if request.user.provider.Provider_type == 1:
        q = Patient.objects.filter(doc_p=request.user.provider)[9:]
    elif request.user.provider.Provider_type == 2:
        q = Patient.objects.filter(doc_d=request.user.provider)[9:]
    elif request.user.provider.Provider_type == 3:
        q = Patient.objects.filter(doc_c=request.user.provider)[9:]
    if request.method == 'POST':
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
                name = setter(request)
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                  "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                  "name10": name[9]})
            else:
                name = setter(request)
                return render(request, 'blogsys/noassigned.html',
                              {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                               "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                               "name10": name[9]})
        else:
            return HttpResponseBadRequest()
    else:
        form = PostQform()
        if len(q) >= 1:
            name = setter(request)
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                              "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                              "name10": name[9]})
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})


def noassigned(request):
    #No Patient assigned list sent to html from above setter
    name = setter(request)
    return render(request, 'blogsys/noassigned.html', {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                       "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                       "name10": name[9]})


def noassigned(request):
    name = setter(request)
    return render(request, 'blogsys/noassigned.html', {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                       "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                       "name10": name[9]})
