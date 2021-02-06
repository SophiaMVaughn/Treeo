from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import PatientRegisterForm, User_Update_Form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #send confirmation email funtion
            #set is active to False
            messages.success(request, f'Account created')
            return redirect('file_upload')
    else:
        form = PatientRegisterForm()
    return render(request, 'register.html', {'form':form})

@login_required
def profile(request):
    return render(request, 'profile.html')
    #this would be required if you dont use @login_required
    # if request.user.is_authenticated:
    #return render(request, 'profile.html')
    # else:
    #     return redirect('/login/?next=%s' % request.path)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        ep = User_Update_Form(request.POST, instance=request.user)
        if ep.is_valid():
            ep.save()
            messages.success(request, f'Edit good')
            return redirect('profile')
    else:
        ep = User_Update_Form(instance=request.user)
    return render(request, 'edit_profile.html', {'edit_profile': ep})


@login_required
def home(request):
    return render(request, 'home.html')
    # logic for different home pages if logged in if not if doc admain ext
