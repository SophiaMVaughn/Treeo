from django import forms
from . import models
from .models import PostQ


class PostQform(forms.Form):
    Message = forms.CharField(widget=forms.Textarea, max_length=200)

    def __init__(self, *args, **kwargs):
        super(PostQform, self).__init__(*args, **kwargs)
        self.fields['Message'].widget.attrs['style'] = 'width:450px; height:80px;'
