from django import forms
from . import models
from .models import ApptTable

class ApptRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApptRequestForm, self).__init__(*args, **kwargs)
        self.fields['provider'].label_from_instance = lambda p: f"{p.firstname} {p.lastname}"

    class Meta:
        model = ApptTable
        #fields = '__all__'
        exclude = ['meetingDate']
