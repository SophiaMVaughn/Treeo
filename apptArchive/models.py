#Nicole

from django.db import models
from ReqAppt.models import *

#Author: Nicole
#This is the ApptArchive table that stores all zoom seesion meetings to the database

class ApptArchive(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    meetingDate = models.DateTimeField(auto_now=False, null=True)

#Author:Nicole
#This is the notes table that stores all created notes to the database

class Notes(models.Model):
    notes = models.CharField(max_length=600)
    apptId = models.ForeignKey(ApptArchive, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

