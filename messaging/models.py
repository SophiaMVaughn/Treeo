from django.db import models
from django.contrib.auth import get_user_model

class message():
    messageID = models.CharField(max_length = 30,  primary_key=True )#auto generate small increment?
    sender = models.CharField(max_length = 40)
    reciever = models.CharField(max_length = 40)
    subject = models.CharField(max_length = 70)
    msgbody = models.CharField(max_length = 700)
    convoID = models.CharField(max_length = 30)#?????????
    # combine into python date time object
    send_time = models.CharField(max_length = 30)
    send_date = models.CharField(max_length = 30)
    #
    read_status = models.CharField(max_length = 10)#bool 1 yes 0 no?
    sender_loc = models.CharField(max_length = 30)#??????????
    reciever_loc = models.CharField(max_length = 30)#?????????
    perm_del = models.CharField(max_length = 5)#purpose??????
