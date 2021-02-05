from django.forms import ModelForm
from .models import Todo
# , Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']

class SignUpForm(UserCreationForm):
    fname = forms.CharField(max_length=30, help_text='Optional.')
    lname = forms.CharField(max_length=30, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'fname', 'lname', 'email', 'password1', 'password2', )