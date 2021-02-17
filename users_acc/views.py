from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
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
#delete later
from messaging.models import *



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
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [m.email],
                fail_silently=False,
            )
            #m.email_user(subject, message)
            return redirect('account_activation_sent')
            #some logic to make sure its actually sent
            #return render(request, 'account_activation_sent.html')
        else:
            return render(request, 'users_acc/register.html', {'form': form})
    else:
        return render(request, 'users_acc/register.html', {'form':PatientRegisterForm()})

def account_activation_sent(request):
    return render(request, 'users_acc/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user =  get_user_model().objects.get(id=uid)
    except (TypeError, ValueError, OverflowError,  get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #user.is_active = True
        user.is_email_confirmed = True
        user.save()
        m=message.objects.create()
        m.sender = user
        m.reciever = user
        m.subject ='Welcome to Treeo'
        m.convoID = 1
        m.read_status = False
        m.sender_loc = 'Outbox'
        m.reciever_loc = 'Inbox'
        m.msgbody = 'Welcome to Treeo'
        m.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users_acc/account_activation_invalid.html')

def button(request):
    if request.method == 'POST':

        #m = get_user_model().objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        m=message.objects.create()
        m.sender = request.user
        m.reciever = request.user
        m.subject ='test'
        m.convoID = 1
        m.read_status = False
        m.sender_loc = 'Outbox'
        m.reciever_loc = 'Inbox'
        m.save()
        return redirect('button')
    else:
        return render(request, 'users_acc/button.html')


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username,password)
        #email or username code need acompying code in model or backend manager to stop @ being used in usernames
        # try:
        #     user = get_user_model().objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        # except get_user_model().DoesNotExist:
        #     get_user_model().set_password(password)
        # except MultipleObjectsReturned:
        #     return get_user_model().objects.filter(email=username).order_by('id').first()
        # else:
        #     if user.check_password(password) and self.user_can_authenticate(user):
        #         return user
        # try:
        #     user = get_user_model().objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        userl = authenticate(request, username=username, password=password)
        if userl is not None:
            #print("test1")
            if userl.is_email_confirmed == True:
                #print("test2")
                login(request, userl)
                #get the stuff or the get responce theing here
                return redirect('home')
            else:
                return render(request, 'users_acc/login.html', {'form': AuthenticationForm(), 'errorMsg': 'Your Account Is Not Confirmed'})
        else:
            return render(request, 'users_acc/login.html', {'form':AuthenticationForm(), 'errorMsg':'Username and password did not match'})
    else:
        return render(request, 'users_acc/login.html', {'form': AuthenticationForm()})




@login_required
def profile(request):
    return render(request, 'users_acc/profile.html')
    #this would be required if you dont use @login_required
    # if request.user.is_authenticated:
    #return render(request, 'profile.html')
    # else:
    #     return redirect('/login/?next=%s' % request.path)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        ep = User_Update_Form(request.POST, instance=request.user)
        if ep.is_valid():
            ep.save()
            messages.success(request, f'Edit good')
            return redirect('profile')
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
            e = Provider.objects.create(user=m,Provider_type=form.cleaned_data.get('providertype'))
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
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [m.email],
                fail_silently=False,
            )
            #m.email_user(subject, message)
            return redirect('account_activation_sent')
            #some logic to make sure its actually sent
            #return render(request, 'account_activation_sent.html')
        else:
            return render(request, 'users_acc/register_provider.html', {'form': form})
    else:
        return render(request, 'users_acc/register_provider.html', {'form':ProviderRegisterForm()})


@login_required
def admin_assign(request):
    if request.method == 'POST':
        ep = AdminAssignForm(request.POST)
        if ep.is_valid():
            pat=ep.cleaned_data.get('patient')
            doc=ep.cleaned_data.get('doc_d')
            doc.Patient_count+=1
            doc.save()
            doc2=ep.cleaned_data.get('doc_c')
            doc2.Patient_count+=1
            doc2.save()
            doc3=ep.cleaned_data.get('doc_p')
            doc3.Patient_count+=1
            doc3.save()
            pat.doc_d=doc
            pat.doc_c=doc2
            pat.doc_p=doc3
            pat.save()
            return redirect('admin_assign')
    else:
        print(Provider.objects.filter(Patient_count__lt=10).filter(Provider_type=1))
        return render(request, 'users_acc/admin_assign.html', {'form':AdminAssignForm()})

@login_required
def admin_remove(request):
    if request.method == 'POST':
        ep = AdminAssignForm(request.POST)
        if ep.is_valid():
            pat=ep.cleaned_data.get('patient')
            doc=ep.cleaned_data.get('doc_d')
            doc.Patient_count-=1
            doc.save()
            doc2=ep.cleaned_data.get('doc_c')
            doc2.Patient_count-=1
            doc2.save()
            doc3=ep.cleaned_data.get('doc_p')
            doc3.Patient_count-=1
            doc3.save()
            pat.doc_d=doc
            pat.doc_c=doc2
            pat.doc_p=doc3
            pat.save()
            return redirect('admin_assign')
    else:
        return render(request, 'users_acc/admin_remove.html', {'form':AdminAssignForm()})


@login_required
def home(request):
    if request.user.user_type == 1:
        return render(request, 'users_acc/home_admin.html')
    elif request.user.user_type == 2:
        return render(request, 'users_acc/home_provider.html')
    elif request.user.user_type == 3:
        return render(request, 'users_acc/home_patient.html')
    # logic for different home pages if logged in if not if doc admain ext
