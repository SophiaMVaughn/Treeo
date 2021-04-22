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
#Author: Brandon
#This is the messaging page code its not different per user it loops to the .
@login_required()
def test2(request):
    context = {}
    master_list=[]
    #we get all the conversations that are for more one user is in doesn't work
    # conversations=Conversation.objects.filter(users=request.user)
    # print(conversations)
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
            context['curconvo'] = request.POST.get("convoid")
            return render(request, 'messaging/index.html', context)
        else:
            context['form'] = MessageForm()
            context['formerrors']= form
            return render(request, 'messaging/index.html', context)
    else:
        return render(request, 'messaging/index.html', context)
