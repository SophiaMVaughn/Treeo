from django import forms
from . import models


class ComposeMessageForm(forms.Form):
    calories = forms.IntegerField()
    subject = forms.CharField(max_length = 70)
    body = forms.CharField(max_length = 600)
class ReplyMessageForm(forms.ModelForm):
    calories = forms.IntegerField()