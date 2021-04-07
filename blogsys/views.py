from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from blogsys.models import PostQ
from .forms import PostQform
from users_acc.models import *


<<<<<<< HEAD
def setter(request):
    name = []
=======


def setter(request):
    name=[]
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
    while (len(name) != 10):
        j = j + 1
        name.append("Patient " + str(j) + " Not Assigned")
=======
    while (len(name)!=10):
        j = j + 1
        name.append("Patient " +str(j)+ " Not Assigned")
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
    return name


# This First Function is a bit long due to it being called and used for both patient and provider.
def Health_Coach(request):
    # If patient

    try:
        if request.user.user_type == 3:
<<<<<<< HEAD
            x = PostQ.objects.filter(Thereciever=(
                request.user.patient.user), Thesender=(request.user.patient.doc_c.user))
            if request.method == 'POST':
                form = PostQform(request.POST)

                if form.is_valid():
                    save = PostQ()
                    save.Message = form.cleaned_data.get('Message')
                    save.Thereciever = (request.user.patient.user)
                    save.TheActualsender = (request.user.patient.user)
                    save.Thesender = (request.user.patient.doc_c.user)
                    save.save()
                    form = PostQform()

                    if request.user.user_type == 3:
                        First = request.user.patient.doc_c.user.first_name
                        Last = request.user.patient.doc_c.user.last_name

                        return render(request, 'blogsys/Health_Coach.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})

=======
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


>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
                    else:
                        return HttpResponseBadRequest()
            else:
                form = PostQform()
                if request.user.user_type == 3:
                    if request.user.user_type == 3:
                        First = request.user.patient.doc_c.user.first_name
                        Last = request.user.patient.doc_c.user.last_name

                        return render(request, 'blogsys/Health_Coach.html',
<<<<<<< HEAD
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
=======
                                    {"form": form, 'PostQ': x, "First": First, "Last": Last})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
    except AttributeError:
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')

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
<<<<<<< HEAD
                        x = PostQ.objects.filter(Thesender=(
                            request.user.provider.user), Thereciever=(q[0].user))
                        return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                         "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                         "name10": name[9]})
=======
                        x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                        return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
                    x = PostQ.objects.filter(Thesender=(
                        request.user.provider.user), Thereciever=(q[0].user))
                    return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                     "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                     "name10": name[9]})
=======
                    x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                    return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316

                else:
                    name = setter(request)
                    return render(request, 'blogsys/noassigned.html',
                                  {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3],
                                   "name5": name[4],
                                   "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                   "name10": name[9]})
<<<<<<< HEAD


def provider(request):
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
=======
def provider(request):
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
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316

                        return render(request, 'blogsys/provider.html',
                                      {"form": form, 'PostQ': x, "First": First, "Last": Last})
    except AttributeError:
        return render(request, 'blogsys/noprovider.html')
    except Exception as e:
        print(e)
        return render(request, 'blogsys/noprovider.html')


def dietitian(request):
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
<<<<<<< HEAD

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


=======


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
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
                name = setter(request)
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient1.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient2(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient2.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD

=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316

def Patient3(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient3.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient4(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient4.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient5(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient5.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient6(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient6.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient7(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient7.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient8(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient8.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient9(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                 "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                 "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                             "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                             "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient9.html', {"form": form, 'PostQ': x, "q":q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD


=======
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
def Patient10(request):
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
<<<<<<< HEAD
                x = PostQ.objects.filter(Thesender=(
                    request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                                  "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                                  "name10": name[9]})
=======
                x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
                return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
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
<<<<<<< HEAD
            x = PostQ.objects.filter(Thesender=(
                request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0], "name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                              "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                              "name10": name[9]})
=======
            x = PostQ.objects.filter(Thesender=(request.user.provider.user), Thereciever=(q[0].user))
            return render(request, 'blogsys/patient10.html', {"form": form, 'PostQ': x, "q": q[0],"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316
        else:
            name = setter(request)
            return render(request, 'blogsys/noassigned.html',
                          {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
<<<<<<< HEAD

=======
def noassigned(request):
    name = setter(request)
    return render(request, 'blogsys/noassigned.html',{"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                           "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                           "name10": name[9]})
>>>>>>> 88244401f48de55ec5f95c9b94f75532a3662316

def noassigned(request):
    name = setter(request)
    return render(request, 'blogsys/noassigned.html', {"name1": name[0], "name2": name[1], "name3": name[2], "name4": name[3], "name5": name[4],
                                                       "name6": name[5], "name7": name[6], "name8": name[7], "name9": name[8],
                                                       "name10": name[9]})
