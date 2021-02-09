from django.db import models
from django.contrib.auth.models import User

class message():
    messageID = models.CharField(max_length = 30,  primary_key=True )
    sender = models.CharField(max_length = 40)
    reciever = models.CharField(max_length = 40)
    subject = models.CharField(max_length = 70)
    msgbody = models.CharField(max_length = 700)
    convoID = models.CharField(max_length = 30)
    send_time = models.CharField(max_length = 30)
    send_date = models.CharField(max_length = 30)
    read_status = models.CharField(max_length = 10)
    sender_loc = models.CharField(max_length = 30)
    reciever_loc = models.CharField(max_length = 30)
    perm_del = models.CharField(max_length = 5)
