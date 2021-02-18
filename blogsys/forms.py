from django import forms
from . import models
from .models import PostQ

class PostQform(forms.Form):
    Name = forms.CharField(max_length=200)
    Message = forms.CharField(max_length=200)



