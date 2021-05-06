from django import forms
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Q
from users_acc.models import *

#Setup Forms
class SetupFormStepOne(forms.Form):
    name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms. CharField(max_length=100)
    email = forms.EmailField()
class SetupFormStepTwo(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)

#Login Forms
class LoginFormStepOne(forms.Form):
    name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms. CharField(max_length=100)
    email = forms.EmailField()
class LoginFormStepTwo(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)

class authentication_form(forms.Form):
    token = forms.IntegerField()

class authentication_form_static(forms.Form):
    token = forms.CharField()

class phone_form(forms.ModelForm):
    phone_no = PhoneNumberField(blank=True, null=True)

    class Meta:
        model = User
        fields = ['phone_no']
        # some labels here for the html
        labels = {
            'phone_no': ('Notification Phone Number'),
        }
