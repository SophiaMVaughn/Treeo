from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from django_otp.decorators import otp_required
import django.utils.timezone
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
#from blogsys.models import *
from ReqAppt.models import *
from messaging.models import *
from utils.tasks import *
from ReqAppt.views import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_otp.plugins.otp_static.models import *

#Author: Brandon
#This is the register funtion it allows people to register as patient users.
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
            #you could also designate a dedicated help account rather than the first admin that is available
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
            return render(request, 'users_acc/register.html', {'form': PatientRegisterForm(),'formerrors': form})
    else:
        return render(request, 'users_acc/register.html', {'form': PatientRegisterForm()})

#Author: Brandon
#This redirects the user to here if the activation was successful.
def account_activation_sent(request):
    return render(request, 'users_acc/account_activation_sent.html')

#Author: Brandon
#This is the activation function processes the link that is sent by email to new users.
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
        login(request, user)
        return render(request, 'users_acc/account_activation_success.html')
    else:
        return render(request, 'users_acc/account_activation_invalid.html')



#Author: Brandon
#This is the login function it logs in users.
def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userl = authenticate(request, username=username, password=password)
        if userl is not None:
            # print("test1")
            if userl.is_email_confirmed == True:
                # test
                if not userl.ota_wait==None and timezone.now()>userl.ota_wait:
                    login(request, userl)
                    return redirect(request.POST.get('next') or request.GET.get('next') or 'home')
                else:
                    login(request, userl)
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

#Author: Brandon
#This is the profile for patient and providers it shows them the details of their accounts.
@otp_required(if_configured=True)
def profile(request):
    return render(request, 'users_acc/profile.html')


#Author: Brandon
#This is the function for edit profile for patient and providers it shows them the details of their accounts and allows them to change them.
@otp_required(if_configured=True)
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

#Author: Brandon
#This allows the admin to register a provider and send them an invite email .
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
            return render(request, 'users_acc/register_provider.html', {'form': ProviderRegisterForm(),'formerrors':form})
    else:
        return render(request, 'users_acc/register_provider.html', {'form': ProviderRegisterForm()})

@otp_required(if_configured=True)
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

#Author: Brandon
#This is the page where we can assign a patient to provider.
@otp_required(if_configured=True)
def admin_display_team(request, id):
    try:
        patient = Patient.objects.get(public_id=id)
    except Exception as e:
        print(e)
        return render(request, "users_acc/admin_assign.html", {'form': AdminAssignForm()})
    else:
        if request.method == 'POST':
            if 'doc_d' in request.POST and not request.POST['doc_d'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_d'])
                    if doc.Patient_count < 10:
                        patient.doc_d = doc
                        patient.save()
                        doc.Patient_count += 1
                        doc.save()
                        # make thread if no thread already exists
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
                    else:
                        return render(request, "users_acc/admin_display_team.html",{'form': AdminProviderUpdateForm(instance=patient), 'patient': patient,'messages': ['Your Account Is Deactivated']})
                except:
                    pass
            else:
                pass
            if 'doc_p' in request.POST and not request.POST['doc_p'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_p'])
                    if doc.Patient_count < 10:
                        patient.doc_p = doc
                        patient.save()
                        doc.Patient_count += 1
                        doc.save()
                        # make thread if no thread already exists
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
                    else:
                        return render(request, "users_acc/admin_display_team.html",{'form': AdminProviderUpdateForm(instance=patient), 'patient': patient,'messages': ['Your Account Is Deactivated']})
                except:
                    pass
            else:
                pass
            if 'doc_c' in request.POST and not request.POST['doc_c'] == '':
                try:
                    doc = get_object_or_404(Provider, id=request.POST['doc_c'])
                    if doc.Patient_count < 10:
                        patient.doc_c = doc
                        patient.save()
                        doc.Patient_count += 1
                        doc.save()
                        # make thread if no thread already exists
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
                    else:
                        return render(request, "users_acc/admin_display_team.html",{'form': AdminProviderUpdateForm(instance=patient), 'patient': patient,'messages': ['Your Account Is Deactivated']})
                except:
                    pass
            else:
                pass
            return render(request, "users_acc/admin_display_team.html", {'form': AdminProviderUpdateForm(instance=patient), 'patient': patient})
        else:
            return render(request, "users_acc/admin_display_team.html", {'form': AdminProviderUpdateForm(instance=patient), 'patient': patient})

#Author: Brandon
#This is the page where we can remove a assigned patient from a provider.
def admin_remove_provider(request, id, id2):
    if request.method == "POST":
        # id = patient id2 =provider
        pat = get_object_or_404(Patient, public_id=id)
        doc = get_object_or_404(Provider, public_id=id2)
        if doc.Provider_type == 1:
            pat.doc_p = None
            pat.save()
            if doc.Patient_count>0:
                doc.Patient_count -= 1
            doc.save()
            # remove thread if empty or dont if messages present
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
            # remove thread if empty or dont if messages present
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
            if doc.Patient_count>0:
                doc.Patient_count -= 1
            doc.save()
            # remove thread if empty or dont if messages present
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
            # remove thread if empty or dont if messages present
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
            if doc.Patient_count>0:
                doc.Patient_count -= 1
            doc.save()
            #remove thread if empty or dont if messages present
            if thread.objects.filter(sender=doc.user, reciever=pat.user).exists():
                print("thread exists")
                test=thread.objects.get(sender=doc.user, reciever=pat.user)
                if message.objects.filter(convoIDt=test).exists():
                    print("messages present")
                else:
                    test.delete()
                    print("no messages deleting conversation")
            else:
                pass
            # remove thread if empty or dont if messages present
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
        return redirect('admin_display_team', pat.public_id)
    context = {'patient': id, 'provider': id2}
    return render(request, "users_acc/deleteconfirm.html", context)
#Author: Brandon
#This is the page where we display the providers and they can be approved or unapproved.
@otp_required(if_configured=True)
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
#Author: Brandon
#This is the page where we can approve providers .
@otp_required(if_configured=True)
def admin_approve_provider(request, id):
    try:
        temp = Provider.objects.get_object_or_404(public_id=id)
    except Exception as e:
        print(e)
        return redirect("admin_approve_provider_render")
    else:
        temp.is_verified=True
        temp.save()
    return redirect("admin_approve_provider_render")
#Author: Brandon
#This is the page where we can unapprove providers.
@otp_required(if_configured=True)
def admin_revoke_provider(request, id):
    try:
        temp = Provider.objects.get_object_or_404(public_id=id)
    except Exception as e:
        print(e)
    else:
        temp.is_verified=False
        temp.save()
    return redirect("admin_approve_provider_render")
#Author: Brandon
#This is the page where an admin can deactivate user accouts .
@otp_required(if_configured=True)
def admin_user_deactivate_render(request):
    temp=User.objects.filter(~Q(user_type= 1))
    if request.method == 'POST':
        print(request.POST)
        if "id" in request.POST:
            id=request.POST.get("id")
            try:
                usertmp = User.objects.get_object_or_404(public_id=id)
                print(usertmp.is_active)
            except Exception as e:
                print(e)
            else:
                usertmp.is_active = False
                usertmp.save()
        elif "id2" in request.POST:
            id=request.POST.get("id2")
            try:
                usertmp = User.objects.get_object_or_404(public_id=id)
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
#Author: Brandon
#This is the page where a user can deactivate thier accout.
@otp_required(if_configured=True)
def user_deactivate(request):
        if request.user.user_type == 3 or request.user.user_type == 2:
            request.user.is_active = False
            request.user.save()
            return render(request, 'users_acc/login.html', {'form': AuthenticationForm(), 'messages': ['Your Account Has Been Deactivated!']})
#Author: Brandon
#This is the page where patient users take the survey.
@otp_required(if_configured=True)
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

#Author: Brandon
#This is the page where patient users take the survey.
@otp_required(if_configured=True)
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
#Author: Brandon
#This is the home page that is personalized baed on the account type of the user.
def home(request):
    if request.user.is_authenticated:
        context={}
        if request.user.user_type == 2:
            context["appointment"] = ApptTable.objects.filter(provider=request.user.provider).order_by("meetingDate")[:2]
            #context["recentMessages"] = PostQ.objects.filter(Thereciever=request.user).order_by("meetingDate")[:2]
        elif request.user.user_type == 3:
            if request.user.patient.survey_status == 1:
                return redirect('take_survey')
            context["appointment"] = ApptTable.objects.filter(patient=request.user.patient).order_by("meetingDate")[:2]
            #context["recentMessages"] = PostQ.objects.filter(Thereciever=request.user).order_by("meetingDate")[:2]
        else:
            context["appointment"] = ApptTable.objects.none
            #context["recentMessages"] = PostQ.objects.none
        return render(request, 'users_acc/home.html',context)
    else:
        return redirect('login')


    
#Author: Gio
#This is the page a patient sees when they view the profile of their dietitian.
@otp_required(if_configured=True)
def dietitian_details(request):
    return render(request, 'users_acc/diet_details.html')
#Author: Gio
#This is the page a patient sees when they view the profile of their pysician.
@otp_required(if_configured=True)
def doctor_details(request):
    return render(request, 'users_acc/doctor_details.html')
#Author: Gio
#This is the page a patient sees when they view the profile of their health coach.
@otp_required(if_configured=True)
def coach_details(request):
    return render(request, 'users_acc/coach_details.html')


#Author: Brandon
#This function request a change of provider.
@otp_required(if_configured=True)
def request_provider_change(request, id):
    doc = Provider.objects.get_object_or_404(public_id=id)
    admin = Admin.objects.first()
    pat=request.user
    if thread.objects.filter(sender=pat, reciever=admin.user).exists():
        curthread=thread.objects.get(sender=pat, reciever=admin.user)
        message.objects.create(convoIDt=curthread, sender=pat, msgbody="I would like to request that a new provider to replace my current "+str(doc.get_Provider_type_display())  +" : "+str(doc.user.get_full_name())+".")
        print("thread exists")
    else:
        curthread=thread.objects.create(sender=pat, reciever=admin.user)
        curthread.save()
        message.objects.create(convoIDt=curthread, sender=pat, msgbody="I would like to request that a new provider to replace my current "+str(doc.get_Provider_type_display())  +" : "+str(doc.user.get_full_name())+".")
        print("thread created")
    messages.success(request, 'Request Sent.')
    return redirect('profile')

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
        m=ApptTable.objects.first()
        archive_apt(m)
        # m.delete()
        # g=get_user_model().objects.first()
        # m=get_user_model().objects.first()
        # thread.objects.create(sender=g, reciever=m)
        # if thread.objects.filter(sender=g, reciever=m).exists():
        #     print("thread exists")
        #     return redirect('button')
        # else:
        #     thread.objects.create(sender=g, reciever=m)
        #     print("thread created")
        #     return redirect('button')
        if not request.user.staticdevice_set.first():
            request.user.staticdevice_set.create(name='backup')
        print(request.user.staticdevice_set.first())
        request.user.staticdevice_set.first().token_set.all().delete()
        for i in range(5):
            request.user.staticdevice_set.first().token_set.create(token=StaticToken.random_token())
        return redirect('button')
    else:
        return render(request, 'users_acc/button.html')


#Author: Brandon
#This a error page handler for 404 errors.
def error_404(request, exception):
    data = {"HTTP_error_message":"404", "HTTP_error_type":"Oops looks like there is nothing here."}
    return render(request, 'users_acc/error_page_base.html', data)

#Author: Brandon
#This a error page handler for 500 errors.


def error_500(request, exception):
    # data = {"HTTP_error_message":"500", "HTTP_error_type":"There was a internal server error."}
    data={}
    return render(request, 'users_acc/error_page_base.html', data)

#Author: Brandon
#This a error page handler for 400 errors.


def error_400(request, exception):
    data = {"HTTP_error_message":"400", "HTTP_error_type":"There was a eternal server error."}
    return render(request, 'users_acc/error_page_base.html', data)

#Author: Brandon
#This a error page handler for 403 errors.


def error_403(request, exception):
    data = {"HTTP_error_message":"403", "HTTP_error_type":"You don't hare permishion to access this data."}
    return render(request, 'users_acc/error_page_base.html', data)

