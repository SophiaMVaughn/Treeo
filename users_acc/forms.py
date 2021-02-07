from django import forms
from django.conf import settings
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
        def save(self, commit=True):
            user = super(PatientRegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.user_type = 1
            if commit:
                user.save()
            return user



# class PatientRegisterForm(UserCreationForm):
#
#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = ('username', 'email')


class User_Update_Form(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']