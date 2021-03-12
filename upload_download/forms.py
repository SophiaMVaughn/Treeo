from django import forms
from .models import *
from users_acc.forms import CustomModelChoiceField
from users_acc.models import *


class Fileform(forms.ModelForm):
    #file = forms.FileField()

    class Meta:
        model = Uploaded_File
        fields = ['file', 'file_type']
        labels = {
            'file': ('File'), 'file_type': ('Type of Document'),
        }

class AdminProviderFileForm(forms.Form):
    provider = CustomModelChoiceField(queryset=(Provider.objects.all()), empty_label="(Select a Provider)")
