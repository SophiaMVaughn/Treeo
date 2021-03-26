from .models import ApptArchive, Notes
from django import forms

class NotesForm(forms.ModelForm):
    notes = forms.CharField(max_length=600)
    #dateAdded= forms.DateTimeField(auto_now=True)
    class Meta:
        model = Notes
        fields = ['notes']