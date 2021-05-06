from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as dauth_views
from . import views as tfa
from django.contrib.auth.views import LoginView
from django_otp.forms import OTPAuthenticationForm

urlpatterns = [
    #what to do about the no path???????
path('', tfa.tfa_profile_view, name='tfa_home'),
path('call/', tfa.verify_phone_call, name='verify_phone_call'),
path('sms/', tfa.verify_phone_message, name='verify_phone_message'),
path('tfa_login/', tfa.tfa_login, name='tfa_login'),
path('verify_authenticaor/', tfa.verify_authenticaor, name='verify_authenticaor'),
path('verify_phone/', tfa.verify_phone, name='verify_phone'),
path('tfa_login_static/', tfa.tfa_login_static, name='tfa_login_static'),
path('tfa_login_phone/', tfa.tfa_login_phone, name='tfa_login_phone'),
path('tfa_login_authenicator/', tfa.tfa_login_authenicator, name='tfa_login_authenicator'),
path('disable_2fa/', tfa.disable_2fa, name='disable_2fa'),
path('enable_2fa/', tfa.enable_2fa, name='enable_2fa'),
path('tfa_profile_view/', tfa.tfa_profile_view, name='tfa_profile_view'),
path('test/', tfa.make_QR_code, name='make_QR_code'),
path('generate_backup_codes/', tfa.generate_backup_codes, name='generate_backup_codes'),
]
