from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    #msgbody = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),max_length=600)
    msgbody = forms.CharField(max_length=600, label='')
    #dateAdded= forms.DateTimeField(auto_now=True)
    class Meta:
        model = message
        fields = ['msgbody']


