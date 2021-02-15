from django import forms
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Q

class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
        def save(self, commit=True):
            user = super(PatientRegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.user_type = 3
            if commit:
                user.save()
            return user


CHOICES= [
    (1, 'Physician'),
    (2, 'Dietician'),
    (3, 'Coach'),
    ]

class ProviderRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    providertype = forms.IntegerField(label='What Type of Provider are You?', widget=forms.Select(choices=CHOICES))
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
        exclude = ('user_type',)
        def save(self, commit=True):
            user = super(PatientRegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.user_type = 2
            if commit:
                user.save()
            return user



class User_Update_Form(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class AdminAssignForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=(Patient.objects.filter(Q(doc_p=None)|Q(doc_d=None)|Q(doc_c=None))), empty_label="(Select a Patient)")
    #now for the selected field in patient if None in doc_ show this ??????????????
    doc_p = forms.ModelChoiceField(queryset=(Provider.objects.filter(Patient_count__lt=10).filter(Provider_type=1)), empty_label="(Select a Physician)")
    doc_d = forms.ModelChoiceField(queryset=(Provider.objects.filter(Patient_count__lt=10).filter(Provider_type=2)), empty_label="(Select a Dietician)")
    doc_c = forms.ModelChoiceField(queryset=(Provider.objects.filter(Patient_count__lt=10).filter(Provider_type=3)), empty_label="(Select a Coach)")
    # class Meta:
    #     model = Patient
    #     fields = ['doc_p','doc_d','doc_c']
    #     def save(self, commit=True):
    #         user = super(PatientRegisterForm, self).save(commit=False)
    #         user.doc_p = self.cleaned_data['doc_p'].id
    #         user.doc_d = self.cleaned_data['doc_d'].id
    #         user.doc_c = self.cleaned_data['doc_c'].id
    #         if commit:
    #             user.save()
    #         return user