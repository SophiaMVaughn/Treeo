from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TodoForm, SignUpForm
from .models import Todo, Profile

# Mail
from smtplib import SMTP
from django.core.mail import send_mail , EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
#send_mail(subject, message, from_email, to_list, dail_silently=True)
# Create your views here.
def home(request):
    # if request.method == 'GET':
    #     send_mail('Welcome to Treeo', 'Test message lorem ipsum', 'tommyesho99@gmail.com', ['tommyesho99@gmail.com'], fail_silently=False)
    #     return render(request, 'todo/home.html')
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':SignUpForm()})
    else:
        # Create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.is_active = False
                user.save()
                # email_subject = 'Welcome to Treeo'
                # email_body = 'Placeholder'
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@treeohealth.com',
                #     [user.email],
                # )
                # email.send(fail_silently=True)
                # subject = 'Welcome to Treeo'
                # message = "Welcome to Treeo!\r\nYou do not have a care team assigned yet, but we'll get one to you ASAP. Let us know if you have any questions.\r\nSincerely,\r\n    Your Treeo Team"
                # from_email = settings.EMAIL_HOST_USER
                # recipient_list = [settings.EMAIL_HOST_USER]
                # send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                # login(request, user)
                # return redirect('currenttodos')
                current_site = get_current_site(request)
                subject = 'Welcome to Treeo'
                message = render_to_string('todo/account_activation_email.html', {
                    'user': user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return redirect('account_activation_sent')
                # return redirect('home')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':SignUpForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            # Tell user password didn't match
            return render(request, 'todo/signupuser.html', {'form':SignUpForm(), 'error':'Passwords did not match'})

def account_activation_sent(request):
    return render(request, 'todo/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'todo/account_activation_invalid.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again'})

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
