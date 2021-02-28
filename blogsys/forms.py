from django import forms
from . import models
from .models import PostQ

class PostQform(forms.Form):
    Message = forms.CharField(max_length=200)


