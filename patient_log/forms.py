from .models import PatientLog
from django import forms

class PatientLogForm(forms.Form):
    calories = forms.IntegerField()
    water = forms.DecimalField(max_digits=7, decimal_places=2)
    blood = forms.DecimalField(max_digits=7, decimal_places=2)
    class Meta:
        model = PatientLog
        fields = '__all__'



