from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from users_acc.models import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def On_create_Patient(sender, instance, created, **kwargs):
    if created:
        #instance.is_active = False
        instance.save()
        if instance.user_type==1:
            Admin.objects.create(user=instance)
        elif instance.user_type==2:
            Physician.objects.create(user=instance)
        elif instance.user_type==3:
            Dietician.objects.create(user=instance)
        elif instance.user_type==4:
            Coach.objects.create(user=instance)
        elif instance.user_type==5:
            Patient.objects.create(user=instance)

#think that this breaks since it can only save patient fix that?
# @receiver(post_save, sender=User)
# def On_save_profile(sender, instance, created, **kwargs):
#     instance.Patient.save()