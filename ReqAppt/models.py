
from django.db import models


class ProviderTable(models.Model):
    id = models.AutoField(primary_key=True, max_length = 50)
    username = models.TextField(max_length = 40 )
    password = models.TextField(max_length = 30 )
    email = models.TextField (max_length = 60)
    firstname = models.TextField (max_length = 40)
    lastname = models.TextField(max_length = 40)
    providerType = models.TextField(max_length = 30)
    creationDate = models.DateTimeField (auto_now = True)
    verified = models.BooleanField(default = True)
    availableTimes = models.TextField(max_length=50)

# create second table apptTable

class ApptTable(models.Model):
    apptId = models.AutoField(primary_key=True, max_length = 50)
    providerType = models.CharField(max_length=40)
    provider = models.ForeignKey(ProviderTable, on_delete=models.CASCADE)
    patientFname = models.CharField(max_length=40)
    patientLname = models.CharField(max_length=40)
    providerType = models.CharField(max_length = 30)
    meetingDate = models.DateTimeField (auto_now = True)


