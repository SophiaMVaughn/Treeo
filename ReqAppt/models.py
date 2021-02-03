from django.db import models

class appt(models.Model):
    ApptTime= models.CharField(max_length=200)
    ProviderName= models.CharField(max_length=200)
    ApptDate=models.CharField(max_length=200)

class scedual(models.Model):
    Appt =models.ForeignKey(appt, on_delete=models.CASCADE)

