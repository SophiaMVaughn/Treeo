from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.conf import settings
from django_otp import devices_for_user, user_has_device, login
from users_acc.models import *
from datetime import timedelta
import django.utils.timezone
from django_otp.plugins.otp_static.models import *
from .forms import *
from formtools.wizard.views import SessionWizardView
import qrcode
import qrcode.image.svg
from django_otp.plugins.otp_totp.models import *
from functools import partial
from django_otp.forms import OTPTokenForm
from binascii import unhexlify
from django_otp.oath import totp
from django.contrib.auth.views import *
from utils.tasks import *
from django.contrib.auth import get_user_model

#important!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#This should be a multi part form using form tools that way we dont have to pass informantion
# between the funtions and could probably combine some of the functions  it might also let us do a staefull approach to incompleate forms rather
# than deleting all the devices each time
#more below with the call funtion

#Author: Brandon
#This is the function gets all of the devices of a user.
def get_devices(user):
    return list(devices_for_user(user, confirmed=False))+list(devices_for_user(user))


def verify_authenticaor(request):
    context = {}
    devices = get_devices(request.user)
    print(devices)
    print(request.user.is_verified())
    if request.method == 'POST':
        form = authentication_form(request.POST)
        if form.is_valid():
            try:
                for device in devices:
                    if isinstance(device, TOTPDevice) and device.name=="authenticator":
                        if device.verify_token(request.POST['token'])==True:
                            device.confirmed=True
                            device.save()
                            request.user.ota_wait = timezone.now() + timedelta(days=30)
                            request.user.save()
                            login(request, device)
                            return render(request, 'users_acc/profile.html', {'messages': ['Your Two Factor Authentication Has Been Activated']})
                        else:
                            return redirect('verify_authenticaor')
            except Exception as e:
                print(e)
        else:
            for device in devices:
                #print(device)
                if isinstance(device, TOTPDevice) and device.name=="authenticator":
                    device.delete()
            context["qr_image"] = reverse('make_QR_code')
            context["authentication_form"] = authentication_form()
            context["messages"] = ['Your Two Factor Authentication Token Is Incorrect. Please Try Again']
            context["formerrors"] = form
            return render(request, 'two_factor_authentication/tfa_authenicator_verify.html', context)
    else:
        #here we remove all previous devices so the user can only have one device of this type
        for device in devices:
            print(device)
            if isinstance(device, TOTPDevice) and device.name=="authenticator":
                device.delete()
        context["qr_image"]=reverse('make_QR_code')
        context["authentication_form"] = authentication_form()
        return render(request, 'two_factor_authentication/tfa_authenicator_verify.html', context)


#Author: Brandon
#This is the function creates the qr code after creating a new device for use with a authenticator app returns responce object of the image.
def make_QR_code(request):
    device = request.user.totpdevice_set.create(confirmed=False, name='authenticator')
    url = device.config_url
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage)
    resp = HttpResponse(content_type='image/svg+xml; charset=utf-8')
    img.save(resp)
    return resp

def verify_phone(request):
    context = {}
    devices = get_devices(request.user)
    print(devices)
    if request.method == 'POST':
        if request.POST['token']:
            print('token')
            form = authentication_form(request.POST)
        elif request.POST['phone_no']:
            print('phone_no')
            form = phone_form(request.POST)
        if form.is_valid():
            try:
                if request.POST['token']:
                    for device in devices:
                        if isinstance(device, PhoneDevice) and device.name=="phone":
                            #print(int(request.POST['token']))
                            if device.verify_token(request.POST['token'])==True:
                                print('token verified')
                                device.confirmed=True
                                device.save()
                                request.user.ota_wait = timezone.now() + timedelta(days=30)
                                request.user.save()
                                login(request, device)
                                return render(request, 'users_acc/profile.html', {'messages': ['Your Two Factor Authentication Has Been Activated']})
                            else:
                                return redirect('verify_phone')
                elif request.POST['phone_form']:
                    print('phone_no')
                    request.user.phone_no = form.cleaned_data.get("phone_no")
                    request.user.save()
                    return redirect('verify_phone')
            except Exception as e:
                print(e)
        else:
            for device in devices:
                #print(device)
                if isinstance(device, PhoneDevice) and device.name=="phone":
                    device.delete()
            return render(request, 'two_factor_authentication/tfa_phone_verify.html', context)
    else:
        #here we remove all previous devices so the user can only have one device of this type
        for device in devices:
            print(device)
            if isinstance(device, PhoneDevice) and device.name=="phone":
                device.delete()
        #might be funtion ot validate the phone number field in the phonnumberfieldmodule didnt have time to look
        if not request.user.phone_no == None and not request.user.phone_no == '':
            print(str(request.user.phone_no.as_national)[-4:])
            context["phone_num"] = str(request.user.phone_no.as_national)[-4:]
            device=request.user.phonedevice_set.create(confirmed=False, name='phone', number=request.user.phone_no.as_e164)
            context["authentication_form"] = authentication_form()
            verify_phone_message(request)
            return render(request, 'two_factor_authentication/tfa_phone_verify.html', context)
        else:
            context["phone_form"] = phone_form()
            return render(request, 'two_factor_authentication/tfa_phone_verify.html', context)


#ok so we can use either of these funtions to contact the user call or sms but
#if you want the user to have an option you will need to probably go with the multipart form i spoke about above
#or some ajax js stuff
#for now you have to change the function  in the code to switch between call and text
def verify_phone_message(request):
    devices = get_devices(request.user)
    for device in devices:
        if isinstance(device, PhoneDevice) and device.name == "phone":
            device.generate_token()
            tfa_message_task(device.id, device.token)

def verify_phone_call(request):
    devices = get_devices(request.user)
    for device in devices:
        if isinstance(device, PhoneDevice) and device.name == "phone":
            device.generate_token()
            tfa_call_task(device.id, device.token)





#Author: Brandon
#This is the function for edit profile for patient and providers it shows them the details of their accounts and allows them to change them.
def tfa_profile_view(request):
    context={}
    if request.user.ota_wait==None:
        return redirect('profile')
    devices=get_devices(request.user)
    backup_codes = []
    for device in devices:
        if isinstance(device, StaticDevice) and device.name == "backup":
            try:
                static_device = request.user.staticdevice_set.first()
                for i in static_device.token_set.all():
                    backup_codes.append(i.token)
                context['backup_codes'] = backup_codes
            except Exception as e:
                print(e)
        elif isinstance(device, PhoneDevice) and device.name=="phone":
            context["phone"] = str(request.user.phone_no.as_national)[-4:]
        elif isinstance(device, TOTPDevice) and device.name=="authenticator":
            context['authenticator'] = ""
    return render(request, 'two_factor_authentication/tfa_profile.html',context)




#Author: Brandon
#This is the function for generating the 5 backup codes.
def generate_backup_codes(request):
    if not request.user.staticdevice_set.first():
        request.user.staticdevice_set.create(name='backup')
    print(request.user.staticdevice_set.first())
    request.user.staticdevice_set.first().token_set.all().delete()
    for i in range(5):
        request.user.staticdevice_set.first().token_set.create(token=StaticToken.random_token())
    return redirect('tfa_profile_view')


# Author: Brandon
#This is the function for enabling a users 2fa by makeing a user device and setting the flag for the user to enabled.
def enable_2fa(request):
    context={}
    if request.user.ota_wait==None:
        return render(request, 'two_factor_authentication/tfa_setup.html', context)
    else:
        return redirect('home')

#Author: Brandon
#This is the function for disabling a users 2fa by deleting the users devices and setting the flag for the user to none.
def disable_2fa(request):
    for i in get_devices(request.user):
        print(i)
        i.delete()
    request.user.ota_wait=None
    request.user.save()
    return redirect('profile')









def tfa_login_static(request):
    context = {'authentication_form': authentication_form_static()}
    devices = get_devices(request.user)
    if request.method == 'POST':
        form = authentication_form_static(request.POST)
        if form.is_valid():
            try:
                for device in devices:
                    if isinstance(device, StaticDevice) and device.name == "backup":
                        if device.verify_token(request.POST['token']) == True:
                            request.user.ota_wait = timezone.now() + timedelta(days=30)
                            request.user.save()
                            login(request, device)
                            return redirect("home")
                        else:
                            context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
                            return render(request, 'two_factor_authentication/tfa_authenticator_login.html',
                                          context)
            except Exception as e:
                print(e)
        else:
            context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
            return render(request, 'two_factor_authentication/tfa_static_login.html', context)
    else:
        return render(request, 'two_factor_authentication/tfa_static_login.html', context)

def tfa_login_phone(request):
    context = {'authentication_form': authentication_form()}
    devices = get_devices(request.user)
    if request.method == 'POST':
        form = authentication_form(request.POST)
        if form.is_valid():
            try:
                for device in devices:
                    if isinstance(device, PhoneDevice) and device.name == "phone":
                        if device.verify_token(request.POST['token']) == True:
                            request.user.ota_wait = timezone.now() + timedelta(days=30)
                            request.user.save()
                            login(request, device)
                            return redirect("home")
                        else:
                            context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
                            return render(request, 'two_factor_authentication/tfa_authenticator_login.html',
                                          context)
            except Exception as e:
                print(e)
        else:
            context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
            return render(request, 'two_factor_authentication/tfa_phone_login.html', context)
    else:
        verify_phone_message(request)
        return render(request, 'two_factor_authentication/tfa_phone_login.html', context)


def tfa_login_authenicator(request):
        context = {'authentication_form':authentication_form()}
        devices = get_devices(request.user)
        if request.method == 'POST':
            form = authentication_form(request.POST)
            if form.is_valid():
                print("test1")
                try:
                    for device in devices:
                        if isinstance(device, TOTPDevice) and device.name == "authenticator":
                            if device.verify_token(request.POST['token']) == True:
                                request.user.ota_wait = timezone.now() + timedelta(days=30)
                                request.user.save()
                                print("test2")
                                login(request, device)
                                return redirect("home")
                            else:
                                context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
                                return render(request, 'two_factor_authentication/tfa_authenticator_login.html',
                                              context)
                except Exception as e:
                    print(e)
            else:
                context['messages'] = ['Incorrect Token. Please Enter Correct Token.']
                return render(request, 'two_factor_authentication/tfa_authenticator_login.html', context)
        else:
            return render(request, 'two_factor_authentication/tfa_authenticator_login.html', context)



#Author: Brandon
#This is the function for loging in via otp.
def tfa_login(request):
    context={}
    devices = get_devices(request.user)
    print(devices)
    for device in devices:
        if isinstance(device, TOTPDevice) and device.name=="authenticator":
            context["authenticator"] ="-"
        if isinstance(device, PhoneDevice) and device.name=="phone":
            context["phone"] ="-"
        if isinstance(device, StaticDevice) and device.name=="backup":
            context["backup"] ="-"
    context["user"] = id
    return render(request, 'two_factor_authentication/tfa_login.html', context)







