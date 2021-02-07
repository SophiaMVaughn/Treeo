from django import forms
from . import models
from .models import ApptTable

class ApptRequestForm(forms.ModelForm):
    class Meta:
        model = ApptTable
        exclude = ['apptId']
