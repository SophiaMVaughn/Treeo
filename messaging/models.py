from django.db import models
from django.contrib.auth import get_user_model

class message():
    #django auto makes a primary key field for id so message.id will get you this
    #ok so this is interesting do the messages have to be scene from the people after the user is deactivated
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reciever = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length = 70)
    msgbody = models.CharField(max_length = 700)
    convoID = models.CharField(max_length = 30)# this is for the reply chanin thing in email thing?????????
    send_time = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField()#1 yes 0 no
    #how does this work?????????????????????????????
    # folder that the user has the message in. inbox sent ect
    sender_loc = models.CharField(max_length = 30)
    # folder that the user has the message in. inbox sent ect
    reciever_loc = models.CharField(max_length = 30)
    # purpose?????? still storeing the mesage in db after the user have deleted it
    perm_del = models.BooleanField()#1 yes 0 no
