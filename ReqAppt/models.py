
from django.db import models
from users_acc.models import *



class ApptTable(models.Model):
    id = models.AutoField(primary_key=True)
    #this needs to be user not patient? thats a redesign i dont want to do
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    meetingDate = models.DateTimeField()
    status = models.BooleanField(default=False)
    meeturlprovider=models.URLField(null=True, max_length=1000)
    meeturlpatient=models.URLField(null=True, max_length=1000)



# class ProviderTable(models.Model):
#     creationDate = models.DateTimeField (auto_now = True)
#     verified = models.BooleanField(default = True)
#     availableTimes = models.TextField(max_length=50)

    # def __str__(self):
    #     return self.firstname + " " + self.lastname
    #     #return 'getProviderValues'

