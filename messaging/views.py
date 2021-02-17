from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models
from django.contrib.auth.decorators import login_required
from . import forms
from .models import *

# Create your views here.
#add chices {for }
#folder= folder the user is looking at default inbox
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

# @login_required
# def folders(request):
#     folder_name=test
#     message_list = message.objects.filter(reciever=request.user,perm_del=False,reciever_loc ='Inbox',reciever_loc = folder_name,)
#     #some kind of page thing
#     return render(request, 'messaging/inbox.html', {'message_list': message_list,})

# @login_required
# def compose(request, recipient=None, form_class=ComposeForm,
#         template_name='django_messages/compose.html', success_url=None,
#         recipient_filter=None):
#     """
#     Displays and handles the ``form_class`` form to compose new messages.
#     Required Arguments: None
#     Optional Arguments:
#         ``recipient``: username of a `django.contrib.auth` User, who should
#                        receive the message, optionally multiple usernames
#                        could be separated by a '+'
#         ``form_class``: the form-class to use
#         ``template_name``: the template to use
#         ``success_url``: where to redirect after successfull submission
#         ``recipient_filter``: a function which receives a user object and
#                               returns a boolean wether it is an allowed
#                               recipient or not
#
#     Passing GET parameter ``subject`` to the view allows pre-filling the
#     subject field of the form.
#     """
#     if request.method == "POST":
#         sender = request.user
#         form = form_class(request.POST, recipient_filter=recipient_filter)
#         if form.is_valid():
#             form.save(sender=request.user)
#             messages.info(request, _(u"Message successfully sent."))
#             if success_url is None:
#                 success_url = reverse('messages_inbox')
#             if 'next' in request.GET:
#                 success_url = request.GET['next']
#             return HttpResponseRedirect(success_url)
#     else:
#         form = form_class(initial={"subject": request.GET.get("subject", "")})
#         if recipient is not None:
#             recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
#             form.fields['recipient'].initial = recipients
#     return render(request, template_name, {
#         'form': form,
#     })
#
# @login_required
# def reply(request, message_id, form_class=ComposeForm,
#         template_name='django_messages/compose.html', success_url=None,
#         recipient_filter=None, quote_helper=format_quote,
#         subject_template=_(u"Re: %(subject)s"),):
#     """
#     Prepares the ``form_class`` form for writing a reply to a given message
#     (specified via ``message_id``). Uses the ``format_quote`` helper from
#     ``messages.utils`` to pre-format the quote. To change the quote format
#     assign a different ``quote_helper`` kwarg in your url-conf.
#
#     """
#     parent = get_object_or_404(Message, id=message_id)
#
#     if parent.sender != request.user and parent.recipient != request.user:
#         raise Http404
#
#     if request.method == "POST":
#         sender = request.user
#         form = form_class(request.POST, recipient_filter=recipient_filter)
#         if form.is_valid():
#             form.save(sender=request.user, parent_msg=parent)
#             messages.info(request, _(u"Message successfully sent."))
#             if success_url is None:
#                 success_url = reverse('messages_inbox')
#             return HttpResponseRedirect(success_url)
#     else:
#         form = form_class(initial={
#             'body': quote_helper(parent.sender, parent.body),
#             'subject': subject_template % {'subject': parent.subject},
#             'recipient': [parent.sender,]
#             })
#     return render(request, template_name, {
#         'form': form,
#     })
#
# @login_required
# def delete(request, message_id, success_url=None):
#     """
#     Marks a message as deleted by sender or recipient. The message is not
#     really removed from the database, because two users must delete a message
#     before it's save to remove it completely.
#     A cron-job should prune the database and remove old messages which are
#     deleted by both users.
#     As a side effect, this makes it easy to implement a trash with undelete.
#
#     You can pass ?next=/foo/bar/ via the url to redirect the user to a different
#     page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
#     """
#     user = request.user
#     now = timezone.now()
#     message = get_object_or_404(Message, id=message_id)
#     deleted = False
#     if success_url is None:
#         success_url = reverse('messages_inbox')
#     if 'next' in request.GET:
#         success_url = request.GET['next']
#     if message.sender == user:
#         message.sender_deleted_at = now
#         deleted = True
#     if message.recipient == user:
#         message.recipient_deleted_at = now
#         deleted = True
#     if deleted:
#         message.save()
#         messages.info(request, _(u"Message successfully deleted."))
#         if notification:
#             notification.send([user], "messages_deleted", {'message': message,})
#         return HttpResponseRedirect(success_url)
#     raise Http404
#
# @login_required
# def undelete(request, message_id, success_url=None):
#     """
#     Recovers a message from trash. This is achieved by removing the
#     ``(sender|recipient)_deleted_at`` from the model.
#     """
#     user = request.user
#     message = get_object_or_404(Message, id=message_id)
#     undeleted = False
#     if success_url is None:
#         success_url = reverse('messages_inbox')
#     if 'next' in request.GET:
#         success_url = request.GET['next']
#     if message.sender == user:
#         message.sender_deleted_at = None
#         undeleted = True
#     if message.recipient == user:
#         message.recipient_deleted_at = None
#         undeleted = True
#     if undeleted:
#         message.save()
#         messages.info(request, _(u"Message successfully recovered."))
#         if notification:
#             notification.send([user], "messages_recovered", {'message': message,})
#         return HttpResponseRedirect(success_url)
#     raise Http404