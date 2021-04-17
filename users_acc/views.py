from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
# Mail
from smtplib import SMTP
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from messaging.models import *
from patient_log.models import *
from blogsys.models import *
from ReqAppt.models import *
from messaging.models import *
from ReqAppt.tasks import *
from ReqAppt.views import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            m = form.save()
            current_site = get_current_site(request)
            subject = 'Welcome to Treeo'
            message = render_to_string('users_acc/account_activation_email.html', {
                'user': form.cleaned_data.get('username'),
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(m.id)),
                'token': account_activation_token.make_token(m),
            })
            #print(subject, message, settings.EMAIL_HOST_USER, m.email)
            send_mail_task.delay(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [m.email],
            )
            #m.email_user(subject, message)
            #you could also designate a dedicated help account
            g=Admin.objects.first()
            if thread.objects.filter(sender=g.user, reciever=m).exists():
                print("thread exists")
            else:
                thread.objects.create(sender=g.user, reciever=m)
                print("thread created")
            if thread.objects.filter(sender=m, reciever=g.user).exists():
                print("thread exists")
            else:
                thread.objects.create(sender=m, reciever=g.user)
                print("thread created")
            return redirect('account_activation_sent')
            # some logic to make sure its actually sent
            # return render(request, 'account_activation_sent.html')
        else:
            return render(request, 'users_acc/register.html', {'form': form})
    else:
        return render(request, 'users_acc/register.html', {'form': PatientRegisterForm()})


def account_activation_sent(request):
    return render(request, 'users_acc/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = get_user_model().objects.get(id=uid)
    except (TypeError, ValueError, OverflowError,  get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #user.is_active = True
        user.is_email_confirmed = True
        user.save()
        # m=message.objects.create()
        # m.sender = user
        # m.reciever = user
        # m.subject ='Welcome to Treeo'
        # m.convoID = 1
        # m.read_status = False
        # m.sender_loc = 'Outbox'
        # m.reciever_loc = 'Inbox'
        # m.msgbody = 'Welcome to Treeo'
        # m.save()
        login(request, user)
        return render(request, 'users_acc/account_activation_success.html')
    else:
        return render(request, 'users_acc/account_activation_invalid.html')

#delete this funtion
def button(request):
    if request.method == 'POST':
        #m = get_user_model().objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # m=message.objects.create()
        # m.sender = request.user
        # m.reciever = request.user
        # m.subject ='test'
        # m.convoID = 1
        # m.read_status = False
        # m.sender_loc = 'Outbox'
        # m.reciever_loc = 'Inbox'
        # m.save()

        # m=ApptTable.objects.first()
        # archive_apt(m.id)
        # m.delete()
        g=get_user_model().objects.first()
        m=get_user_model().objects.first()
        thread.objects.create(sender=g, reciever=m)
        # if thread.objects.filter(sender=g, reciever=m).exists():
        #     print("thread exists")
        #     return redirect('button')
        # else:
        #     thread.objects.create(sender=g, reciever=m)
        #     print("thread created")
        #     return redirect('button')
        return redirect('button')
    else:
        return render(request, 'users_acc/button.html')


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userl = authenticate(request, username=username, password=password)
        if userl is not None:
            # print("test1")
            if userl.is_email_confirmed == True:
                # print("test2")
                login(request, userl)
                # get the stuff or the get responce theing here
                return redirect(request.POST.get('next') or request.GET.get('next') or 'home')
            else:
                return render(request, 'users_acc/login.html', {'form': AuthenticationForm(), 'messages': ['Your Account Is Not Confirmed']})
        else:
            if User.objects.get(username=username).is_active == False:
                return render(request, 'users_acc/login.html',{'form': AuthenticationForm(), 'messages': ['Your Account Is Deactivated']})
            else:
                return render(request, 'users_acc/login.html', {'form': AuthenticationForm(), 'messages': ['Username and password did not match']})
    else:
        return render(request, 'users_acc/login.html', {'form': AuthenticationForm()})


@login_required
def profile(request):
    return render(request, 'users_acc/profile.html')
    # this would be required if you dont use @login_required
    # if request.user.is_authenticated:
    # return render(request, 'profile.html')
    # else:
    #     return redirect('/login/?next=%s' % request.path)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        #form = User_Update_Form(request.POST or None)
        ep = User_Update_Form(request.POST, request.FILES, instance=request.user)
        if ep.is_valid():
            request.user.username = ep.cleaned_data.get("username")
            request.user.email = ep.cleaned_data.get("email")
            request.user.first_name = ep.cleaned_data.get("first_name")
            request.user.last_name = ep.cleaned_data.get("last_name")
            request.user.phone_no = ep.cleaned_data.get("phone_no")
            request.user.profile_pic = ep.cleaned_data.get("profile_pic")
            request.user.save()
            #print("test")
            # ep.save()
            #
            return redirect('profile')
        else:
            #print some error for validation of stuff
            #print(ep.errors)
            form = User_Update_Form(instance=request.user)
            return render(request, 'users_acc/edit_profile.html', {'edit_profile': form,'formerrors': ep})
    else:
        ep = User_Update_Form(instance=request.user)
    return render(request, 'users_acc/edit_profile.html', {'edit_profile': ep})


def doctor_registration(request):
    if request.method == 'POST':
        form = ProviderRegisterForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.user_type = 2
            m.save()
            e = Provider.objects.create(
                user=m, Provider_type=form.cleaned_data.get('providertype'))
            e.save()
            current_site = get_current_site(request)
            subject = 'Welcome to Treeo'
            message = render_to_string('users_acc/account_activation_email.html', {
                'user': form.cleaned_data.get('username'),
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(m.id)),
                'token': account_activation_token.make_token(m),
            })
            #print(subject, message, settings.EMAIL_HOST_USER, m.email)
            send_mail_task.delay(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [m.email],
            )
            #m.email_user(subject, message)
            return redirect('account_activation_sent')
            # some logic to make sure its actually sent
            # return render(request, 'account_activation_sent.html')
        else:
            return render(request, 'users_acc/register_provider.html', {'form': form})
    else:
        return render(request, 'users_acc/register_provider.html', {'form': ProviderRegisterForm()})

@login_required
def admin_view(request):
    # if request.method == 'POST':
    #     form = AdminAssignForm(request.POST)
    #     if form.is_valid():
    #         patient = Patient.objects.none()
    #         try:
    #             patient = Patient.objects.get(id=request.POST['patient'])
    #         except Exception as e:
    #             print(e)
    #             return render(request, "users_acc/admin_assign.html", {'form': AdminAssignForm()})
    #         else:
    #             return redirect('admin_display_team', request.POST['patient'])
    #     else:
    #         return render(request, "users_acc/admin_assign.html", {'form': AdminAssignForm(),'formerrors': form})
    # else:
    patient = Patient.objects.all()
    pagination = Paginator(patient, 5)
    page = request.GET.get('page', 1)
    try:
        pagination = pagination.page(page)
    except PageNotAnInteger:
        pagination = pagination.page(1)
    except EmptyPage:
        pagination = pagination.page(pagination.num_pages)
    # general except 501????
    context = {
        'patients': pagination
    }
    return render(request, "users_acc/admin_assign.html", context)


@login_required
def admin_display_team(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Exception as e:
        print(e)
        return render(request, "users_acc/admin_assign.html", {'form': AdminAssignForm()})
    else:
        if request.method == 'POST':
            if 'doc_d' in request.POST and not request.POST['doc_d'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_d'])
                    patient.doc_d = doc
                    patient.save()
                    doc.Patient_count += 1
                    doc.save()
                    if thread.objects.filter(sender=doc.user, reciever=patient.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=doc.user, reciever=patient.user)
                    if thread.objects.filter(sender=patient.user, reciever=doc.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=patient.user, reciever=doc.user)
                except:
                    pass
            else:
                pass
            if 'doc_p' in request.POST and not request.POST['doc_p'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_p'])
                    patient.doc_p = doc
                    patient.save()
                    doc.Patient_count += 1
                    doc.save()
                    if thread.objects.filter(sender=doc.user, reciever=patient.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=doc.user, reciever=patient.user)
                    if thread.objects.filter(sender=patient.user, reciever=doc.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=patient.user, reciever=doc.user)
                except:
                    pass
            else:
                pass
            if 'doc_c' in request.POST and not request.POST['doc_c'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_c'])
                    patient.doc_c = doc
                    patient.save()
                    doc.Patient_count += 1
                    doc.save()
                    if thread.objects.filter(sender=doc.user, reciever=patient.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=doc.user, reciever=patient.user)
                    if thread.objects.filter(sender=patient.user, reciever=doc.user).exists():
                        print("thread exists")
                        pass
                    else:
                        thread.objects.create(sender=patient.user, reciever=doc.user)
                except:
                    pass
            else:
                pass
            return render(request, "users_acc/admin_display_team.html", {'form': AdminProviderUpdateForm(instance=patient), 'patient': patient})
        else:
            return render(request, "users_acc/admin_display_team.html", {'form': AdminProviderUpdateForm(instance=patient), 'patient': patient})


def admin_remove_provider(request, id, id2):
    if request.method == "POST":
        # id = patient id2 =provider
        pat = get_object_or_404(Patient, id=id)
        doc = get_object_or_404(Provider, id=id2)
        if doc.Provider_type == 1:
            pat.doc_p = None
            pat.save()
            doc.Patient_count -= 1
            doc.save()
            if thread.objects.filter(sender=doc.user, reciever=pat.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=doc.user, reciever=pat.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
            if thread.objects.filter(sender=pat.user, reciever=doc.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=pat.user, reciever=doc.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
        if doc.Provider_type == 2:
            pat.doc_d = None
            pat.save()
            doc.Patient_count -= 1
            doc.save()
            if thread.objects.filter(sender=doc.user, reciever=pat.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=doc.user, reciever=pat.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
            if thread.objects.filter(sender=pat.user, reciever=doc.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=pat.user, reciever=doc.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
        if doc.Provider_type == 3:
            pat.doc_c = None
            pat.save()
            doc.Patient_count -= 1
            doc.save()
            if thread.objects.filter(sender=doc.user, reciever=pat.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=doc.user, reciever=pat.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
            if thread.objects.filter(sender=pat.user, reciever=doc.user).exists():
                print("thread exists")
                #try except here
                test=thread.objects.get(sender=pat.user, reciever=doc.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
        return redirect('admin_display_team', pat.id)
    context = {'patient': id, 'provider': id2}
    return render(request, "users_acc/deleteconfirm.html", context)

@login_required
def admin_approve_provider_render(request):
    temp=Provider.objects.filter().order_by('is_verified')
    pagination = Paginator(temp, 5)
    page = request.GET.get('page', 1)
    try:
        pagination = pagination.page(page)
    except PageNotAnInteger:
        pagination = pagination.page(1)
    except EmptyPage:
        pagination = pagination.page(pagination.num_pages)
    # general except 501????
    context = {
        'results': pagination
    }
    return render(request, "users_acc/admin_approve_provider.html", context)

@login_required
def admin_approve_provider(request, id):
    try:
        temp = Provider.objects.get(id=id)
    except Exception as e:
        print(e)
        return redirect("admin_approve_provider_render")
    else:
        temp.is_verified=True
        temp.save()
    return redirect("admin_approve_provider_render")

@login_required
def admin_revoke_provider(request, id):
    try:
        temp = Provider.objects.get(id=id)
    except Exception as e:
        print(e)
    else:
        temp.is_verified=False
        temp.save()
    return redirect("admin_approve_provider_render")

@login_required
def admin_user_deactivate_render(request):
    temp=User.objects.filter(~Q(user_type= 1))
    if request.method == 'POST':
        print(request.POST)
        if "id" in request.POST:
            id=request.POST.get("id")
            try:
                usertmp = User.objects.get(id=id)
                print(usertmp.is_active)
            except Exception as e:
                print(e)
            else:
                usertmp.is_active = False
                usertmp.save()
        elif "id2" in request.POST:
            id=request.POST.get("id2")
            try:
                usertmp = User.objects.get(id=id)
                print(usertmp.is_active)
            except Exception as e:
                print(e)
            else:
                usertmp.is_active = True
                usertmp.save()
        pagination = Paginator(temp, 5)
        page = request.GET.get('page', 1)
        try:
            pagination = pagination.page(page)
        except PageNotAnInteger:
            pagination = pagination.page(1)
        except EmptyPage:
            pagination = pagination.page(pagination.num_pages)
        # general except 501????
        context = {
            'results': pagination
        }
        return render(request, "users_acc/admin_deactivate_user.html", context)
    else:
        pagination = Paginator(temp, 5)
        page = request.GET.get('page', 1)
        try:
            pagination = pagination.page(page)
        except PageNotAnInteger:
            pagination = pagination.page(1)
        except EmptyPage:
            pagination = pagination.page(pagination.num_pages)
        # general except 501????
        context = {
            'results': pagination
        }
        return render(request, "users_acc/admin_deactivate_user.html", context)

@login_required
def user_deactivate(request):
        if request.user.user_type == 3 or request.user.user_type == 2:
            request.user.is_active = False
            request.user.save()
            return render(request, 'users_acc/login.html', {'form': AuthenticationForm(), 'messages': ['Your Account Has Been Deactivated!']})

@login_required
def take_survey(request):
    if request.user.user_type ==3:
        if request.user.patient.survey_status==1:
            if request.method == 'POST':
                if "flag" in request.POST:
                    print(request.POST.get('flag'))
                    return redirect("render_survey")
                elif "flag2" in request.POST:
                    print(request.POST.get('flag2'))
                    request.user.patient.survey_status = 3
                    request.user.patient.save()
                    return redirect("home")
                else:
                    print(request.POST)
                    return redirect("home")
            else:
                return render(request, 'users_acc/takesurvey.html')
        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required
def render_survey(request):
    if request.user.user_type ==3:
        if request.user.patient.survey_status==1:
            if request.method == 'POST':
                #is valid
                #save data of results
                #??????
                if "txtinput" in request.POST:
                    request.user.patient.survey_info = request.POST.get('txtinput')
                    request.user.patient.survey_status = 2
                    request.user.patient.save()
                    return redirect("home")
                else:
                    return redirect("home")
            else:
                return render(request, 'users_acc/survey.html')
        else:
            return redirect("home")
    else:
        return redirect("home")

def home(request):
    if request.user.is_authenticated:
        context={}
        if request.user.user_type == 2:
            context["appointment"] = ApptTable.objects.filter(provider=request.user.provider).order_by("meetingDate")[:2]
            context["recentMessages"] = PostQ.objects.filter(Thereciever=request.user).order_by("-meetingDate")[:2]
        elif request.user.user_type == 3:
            context["appointment"] = ApptTable.objects.filter(patient=request.user.patient).order_by("meetingDate")[:2]
            context["recentMessages"] = PostQ.objects.filter(Thereciever=request.user).order_by("-meetingDate")[:2]
        else:
            context["appointment"] = ApptTable.objects.none
            context["recentMessages"] = PostQ.objects.none
        return render(request, 'users_acc/home.html',context)
    else:
        return redirect('login')


    
#coales to one view and add error handling
@login_required
def dietitian_details(request):
    return render(request, 'users_acc/diet_details.html')

@login_required
def doctor_details(request):
    return render(request, 'users_acc/doctor_details.html')

@login_required
def coach_details(request):
    return render(request, 'users_acc/coach_details.html')


