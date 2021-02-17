from django import forms
from . import models
from .models import ApptTable
from users_acc.models import *
import itertools
class ApptRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApptRequestForm, self).__init__(*args, **kwargs)
        self.fields['patient'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"
        self.fields['provider'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"


    class Meta:
        model = ApptTable
        #fields = '__all__'
        exclude = ['meetingDate', 'status']

#class ApptRequestFormDoc(forms.ModelForm):
    #patient = forms.ModelChoiceField(queryset=(Patient.objects.filter(doc_d='dsfg')), empty_label="(Select a Patient)")
    # def __init__(self, *args, **kwargs):
    #     super(ApptRequestForm, self).__init__(*args, **kwargs)
    #     exclude = ('created_by',)
    #     self.fields['patient'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"
    #     self.fields['provider'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"

    # class Meta:
    #     model = ApptTable
    #     #fields = '__all__'
    #     exclude = ['meetingDate', 'status']

class ApptRequestFormPatient(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApptRequestForm, self).__init__(*args, **kwargs)
        del self.fields['patient']
        self.fields['patient'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"
        self.fields['provider'].label_from_instance = lambda p: f"{p.user.first_name} {p.user.last_name}"
        # del self.fields['patient']


    class Meta:
        model = ApptTable
        #fields = '__all__'
        exclude = ['meetingDate', 'status']