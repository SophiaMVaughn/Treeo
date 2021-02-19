from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models
from django.contrib.auth.decorators import login_required
from . import forms
from .models import *


#add chices {for }
#folder= folder the user is looking at default inbox not neeeded as its a conversation thing???
#all messages that the user recieved that aren't perminitly deleted and that arte in the current folder
#mabye make a list of all of the messages that the user recieved that aren't perminitly deleted = john
# and then querry john for everything that is for the folder?????
#folder=message.objects.filter(reciever = request.user).filter(perm_del = 0).filter(reciever_loc = "folder")

@login_required
def inbox(request):
    message_list = message.objects.filter(reciever=request.user).order_by('send_time')
    #this should return list of converastion and then render the one that is clicked on
    return render(request, 'messaging/inbox.html', {'message_list': message_list})

@login_required
def render_conversation(request, convo_id):
    message_list = message.objects.filter(reciever=request.user, convoID=convo_id).order_by('send_time')
    if message_list:
        for i in message_list:
            i.read_status=1
            i.save()
    #change all messages in convo to read
    return render(request, 'messaging/inbox.html', {'message_list': message_list})

@login_required
def list_conversation_active(request):
    message_list = message.objects.filter(reciever=request.user,perm_del=False).values_list('convoID').distinct()
    if message_list:
        for i in message_list:
            #order by read and see if firset
            message_list = message.objects.filter(reciever=request.user, perm_del=False, convoID=i[0]).order_by('send_time').first()
            print(message_list)
    # print(convo id,reciever,sender ,if unread messages, subject????)
        #does this need to return or just
    return render(request, 'messaging/inbox.html', {'message_list': message_list})


@login_required
def list_conversation_deleted(request):
    #true if one deleted method???????????
    message_list = message.objects.filter(reciever=request.user,perm_del=True).values_list('convoID').distinct()
    if message_list:
        for i in message_list:
            message_list = message.objects.filter(reciever=request.user, perm_del=False, convoID=i[0]).order_by('send_time').first()
            print(message_list)
    # print(convo id,reciever,sender ,if unread messages)
        #does this need to return or just
    return render(request, 'messaging/inbox.html', {'message_list': message_list})



@login_required
def delete_conversation(request, convo_id):
    message_list = message.objects.filter(reciever=request.user,perm_del=False, convoID=convo_id)
    if message_list:
        for i in message_list:
            i.perm_del=1
            i.save()
    return redirect('messaging_home')


@login_required
def undelete_conversation(request, convo_id):
    message_list = message.objects.filter(reciever=request.user,perm_del=True, convoID=convo_id)
    if message_list:
        for i in message_list:
            i.perm_del=0
            i.save()
    return redirect('messaging_home')

@login_required
def delete_message(request, id):
    message_list = message.objects.filter(id=id)
    print(message_list)
    if message_list:
        for i in message_list:
            i.perm_del=1
            i.save()
            #change to redirect
            return render_conversation(request, i.convoID)
    else:
        return redirect('messaging_home')

@login_required
def undo_delete(request, id):
    message_list = message.objects.filter(id=id)
    if message_list:
        for i in message_list:
            print(i.perm_del)
            i.perm_del=0
            i.save()
            return render_conversation(request, i.convoID)
    else:
        return redirect('messaging_home')

@login_required
def unread_count(request):
    message_list = message.objects.filter(reciever=request.user,perm_del=False, read_status=0)
    if len(message_list)>0:
        return len(message_list)
    else:
        return 0

@login_required
def new_convo(request):
    # use a form with the error checking for proifanity here
    m = message.objects.create()
    m.sender = request.user
    m.reciever = form.stuff
    m.subject = form.stuff
    # auto increments so not needed m.convoID = convo_id
    m.read_status = True
    m.sender_loc = 'Outbox'
    m.reciever_loc = 'Inbox'
    m.save()

@login_required
def reply(request, ):
    # use a form with the error checking for proifanity here
    m = message.objects.create()
    m.sender = request.user
    m.reciever = recipient
    m.subject = form.stuff
    m.convoID = convo_id
    m.read_status = True
    m.sender_loc = 'Outbox'
    m.reciever_loc = 'Inbox'
    m.save()
