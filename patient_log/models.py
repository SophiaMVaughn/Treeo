from django.db import models

#blood_category ={
               #('red blood cells', 'red blood cells'),
                #('white blood cells', 'white blood cells'),
                #('platelets', 'platelets'),
                #('hemoglobin', 'hemoglobin'),
                #('hematocrit', 'hematocrit'),
                #}

class PatientLog(models.Model):
    calories = models.IntegerField(default=0)
    water = models.DecimalField(max_digits=5, decimal_places=2)
    blood = models.DecimalField(max_digits=5, decimal_places=2)
    #date = models.DateTimeField(auto_now_add = True)



