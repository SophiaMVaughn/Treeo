from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models
from django.contrib.auth.decorators import login_required
import json
from .forms import *
from .models import *
from users_acc.models import *
from django.core import serializers
import datetime

# master list is a list of all the conversations ie a set(stored as a list) of lists with each list in the set having of all of the messages
# from one other user to the current logged in user
# how do we handle empty messages since we can derive user data from already sent messages  but if there are no messages between 2 users we cant start a conversation
# options start each user off with a default welcome message when the docs are assigned a patient and when a care team is assigned to a patient?
# or we can send tuples with the user and messages(user,messages) with some having [] messages
#  neither approach  handles former patients however so perhapse another idea is
# could also be mitigated with a list of stored converation threads so we dont have to  where we get those check if any
# new patients are assigned and add new ones doesnt cover threads made by mistake
# this is not an expected use case but stillwe can mitigate it by having you can have empty threads be deleted on removal of provider

@login_required()
def test(request):
    context={}
    data = serializers.serialize("json", message.objects.all())
    data2 = serializers.serialize("json", User.objects.filter(id=1), fields=["first_name", "last_name", "profile_pic","username"])
    #list of everyone who they are syuposed to talk to and all of the messages between those people and all of the messages that are in thier
    #or list of all conversation objects and those have all the info we need and they can be derived from
    # serializers.serialize("json", User.objects.filter(id=2),fields=["first_name", "last_name", "profile_pic", "username"])
    # serializers.serialize("json", User.objects.all(), fields=["first_name", "last_name", "profile_pic", "username"])
    # use the 3 tubles with one being a list of message objects one being the usernot nessicary??? depends if yiou go for the  and one being the conversationo eject
    thistuple = (data2, data)
    thistuple2 = (data2, data,)
    thistuple3 = (data2, data,)
    x=[thistuple,thistuple2,thistuple3]
    context['message_all'] = json.dumps(x)
    context['message_none'] = message.objects.none()
    context['user_all'] = User.objects.first()
    context['user_none'] = User.objects.none()
    context['user'] = message.objects.all()
    context['form'] = MessageForm()
# you must sort by the tent time for the querry set of messages
    return render(request, 'messaging/index.html', context)

@login_required()
def test2(request):
    context = {}
    master_list=[]
    # ok conversations when a user call for chat what happens???
    #we get all the conversations that thye are in so
    conversations=Conversation.objects.filter(users=request.user)
    print(conversations)
    threads=thread.objects.filter(reciever=request.user)
    print(threads)
    #or i in convos
    for i in threads:
        #get messages with that thread/convo id and store them in a list and make a tuple and add that to the master list
        temptuple = (i, message.objects.filter(convoIDt=i).order_by("send_time"))
        master_list.append(temptuple)
    print(master_list)
    context['master_list'] = master_list
    context['form'] = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                #** form.cleaned_data
                #msgbody=form.cleaned_data.get("msgbody")
                mes = message.objects.create(msgbody=form.cleaned_data.get("msgbody"), sender=request.user, convoIDt=thread.objects.get(id=request.POST.get("convoid")))
                mes.save()
            except Exception as e:
                print(e)
                return render(request, 'messaging/index.html', context)
            context = {}
            master_list = []
            # ok conversations when a user call for chat what happens???
            # we get all the conversations that thye are in so
            conversations = Conversation.objects.filter(users=request.user)
            print(conversations)
            threads = thread.objects.filter(reciever=request.user)
            print(threads)
            # or i in convos
            for i in threads:
                # get messages with that thread/convo id and store them in a list and make a tuple and add that to the master list
                temptuple = (i, message.objects.filter(convoIDt=i).order_by("send_time"))
                master_list.append(temptuple)
            print(master_list)
            context['master_list'] = master_list
            context['form'] = MessageForm()
            return render(request, 'messaging/index.html', context)
        else:
            return render(request, 'messaging/index.html', context)
    else:
        return render(request, 'messaging/index.html', context)
