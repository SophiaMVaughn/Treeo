from django.db import models



class appt(models.Model):
    doctor=models.CharField(max_length=70,null=True)
    Time = models.CharField(max_length=70, null=True)
    patientNum = models.PositiveIntegerField(null=True)
    doctorNum = models.PositiveIntegerField(null=True)
    Date=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    patient = models.CharField(max_length=70, null=True)
