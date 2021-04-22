from .models import ApptArchive, Notes
from django import forms
from users_acc.Validator import *

class NotesForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea,max_length=600, validators=[validate_profanity])
    #dateAdded= forms.DateTimeField(auto_now=True)
    class Meta:
        model = Notes
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.fields['notes'].widget.attrs['style'] = 'width:675px; height:135px;'