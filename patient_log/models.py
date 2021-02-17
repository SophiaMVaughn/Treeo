from django.db import models
from users_acc.models import *

#blood_category ={
               #('red blood cells', 'red blood cells'),
                #('white blood cells', 'white blood cells'),
                #('platelets', 'platelets'),
                #('hemoglobin', 'hemoglobin'),
                #('hematocrit', 'hematocrit'),
                #}

class PatientLog(models.Model):
    #forin key to patient
    calories = models.IntegerField(default=0)
    water = models.DecimalField(max_digits=5, decimal_places=2)
    blood = models.DecimalField(max_digits=5, decimal_places=2)
    #date = models.DateTimeField(auto_now_add = True)




