from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=User)
def On_create_Patient(sender, instance, created, **kwargs):
    if created:
        #add some logic so the correct profile is initiated based on the account identifier number 123456789ect
        Patient.objects.create(user=instance)

#think that this breaks since it can only save patient fix that?
# @receiver(post_save, sender=User)
# def On_save_profile(sender, instance, created, **kwargs):
#     instance.Patient.save()