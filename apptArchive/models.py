from django.db import models
from ReqAppt.models import *

class ApptArchive(models.Model):
    apptId = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    meetingDate = models.DateTimeField(auto_now=False)

class Notes(models.Model):
    notes = models.CharField(max_length=600)
    apptId = models.ForeignKey(ApptArchive, on_delete=models.CASCADE)

