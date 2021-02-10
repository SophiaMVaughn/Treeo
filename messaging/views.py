from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
#add chices {for }
#folder= folder the user is looking at default inbox
#all messages that the user recieved that aren't perminitly deleted and that arte in the current folder
#mabye make a list of all of the messages that the user recieved that aren't perminitly deleted = john
# and then querry john for everything that is for the folder?????
#folder=message.objects.filter(reciever = request.user).filter(perm_del = 0).filter(reciever_loc = "folder")
