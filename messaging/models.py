from django.db import models
from django.contrib.auth import get_user_model
class thread(models.Model):

    # sender and reciever are more like user one or two not indicative a orole
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='t_sender', null=True, blank=True)
    reciever = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='t_reciever', null=True,blank=True)
    last_message_time = models.DateTimeField(auto_now_add=True)
    # 1 yes 0 no
    unread_messages = models.IntegerField(default=0)





class ConversationUserThrough(models.Model):
    channel = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Conversation(models.Model):
    users = models.ManyToManyField(get_user_model(), blank=True, through=ConversationUserThrough, related_name='conversation_members')
    last_message_time = models.DateTimeField(auto_now_add=True)
    # 1 yes 0 no
    unread_messages = models.IntegerField(default=0)



# get rid of subject and then add it to the tread??????????
class message(models.Model):
    convoIDt = models.ForeignKey(thread, on_delete=models.CASCADE, related_name='thread', null=True, blank=True)
    convoID = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='convoID', null=True, blank=True)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    # subject = models.CharField(max_length=70)
    msgbody = models.CharField(max_length=600)
    send_time = models.DateTimeField(auto_now_add=True)
    # instead of read status have read time default to nul so if not read then null and if read the delivered or just keep it as binary
    read_status = models.BooleanField(default=False)  # 1 yes 0 no
    # this would allow us to store the mesage in db after the user decides to deleted it to allow and for undelete, gives the illusion of deletion more or less we would modify the queries  to only display mesages not permdeleted
    # 1 yes 0 no
    #perm_del = models.BooleanField(default=False)







