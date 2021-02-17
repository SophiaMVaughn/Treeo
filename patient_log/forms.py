from .models import PatientLog, Provider
from django import forms
from django.db import models

class PatientLogForm(forms.Form):
    calories = forms.IntegerField()
    water = forms.DecimalField(max_digits=7, decimal_places=2)
    blood = forms.DecimalField(max_digits=7, decimal_places=2)
    doc_d = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='doc_d', null=True)
    class Meta:
        model = PatientLog
        fields = '__all__'



