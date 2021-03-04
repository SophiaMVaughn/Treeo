from .models import PatientLog
from django import forms
from django.db import models
from users_acc.forms import CustomModelChoiceField
from users_acc.models import *
from django.db.models import Q

class PatientLogForm(forms.Form):
    calories = forms.IntegerField(label='Enter your calories for the day', widget = forms.TextInput)
    water = forms.DecimalField(label='Enter your daily water intake(oz)', widget = forms.TextInput, max_digits=7, decimal_places=2)
    sleep = forms.DecimalField(label= 'How many hours of sleep (hrs)', widget = forms.TextInput,  max_digits=7, decimal_places=2)
    mood = forms.IntegerField(label='What is your current mood (rate 1-5)', widget=forms.TextInput)
    class Meta:
        model = PatientLog
        fields = fields = ['calories', 'water', 'sleep','mood']


class AdminProviderLogForm(forms.Form):
    patient = CustomModelChoiceField(queryset=(Patient.objects.all()), empty_label="(Select a Patient)")
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance")
        #super(ApptRequestForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        if instance.user.user_type == 2:
            q = Provider.objects.none()
            if instance.user.provider.Provider_type ==1:
                q = Patient.objects.filter(doc_p=instance.user.provider)
            elif instance.user.provider.Provider_type ==2:
                q = Patient.objects.filter(doc_d=instance.user.provider)
            elif instance.user.provider.Provider_type ==3:
                q = Patient.objects.filter(doc_c=instance.user.provider)
            self.fields['patient']=CustomModelChoiceField(queryset=(q), empty_label="(Select a Patient)")
        elif instance.user.user_type == 1:
            self.fields['patient'] = CustomModelChoiceField(queryset=(Patient.objects.all()),empty_label="(Select a Patient)")
        else:
            self.fields['patient'] = CustomModelChoiceField(queryset=(Patient.objects.none()),empty_label="(Select a Patient)")
