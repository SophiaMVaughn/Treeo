from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    # if you cant have more than one role
    # USER_TYPE_OPTIONS = ((1, 'student'),(2, 'teacher'),(3, 'secretary'),(4, 'supervisor'),(5, 'admin'),)
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
        def save(self, commit=True):
            user = super(PatientRegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit:
                user.save()
            return user

class User_Update_Form(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']