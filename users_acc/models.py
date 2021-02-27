from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
#from .managers import CustomUserManager


USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Provider'),
        (3, 'Patient'),
    )
PROVIDER_TYPE_CHOICES = (
        (1, 'Physician'),
        (2, 'Dietician'),
        (3, 'Coach'),
    )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=3)
    is_staff = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    phone_no = models.CharField(max_length = 10, default='')
    # profile_pic = models.ImageField(default=profile.png, upload_to='profile_pictures')
    #objects = CustomUserManager()
# #   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#acess via
# provider.user.last_name.
# user.related profile name.Patient_count
#patientobj.doc_d.user.last_name


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="admin", on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.user.first_name+" "+self.user.last_name

class Provider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="provider", on_delete=models.CASCADE)
    Patient_count = models.PositiveSmallIntegerField(default=0)
    Provider_type = models.PositiveSmallIntegerField(choices=PROVIDER_TYPE_CHOICES,default=1)
    # def __str__(self):
    #     return self.user.first_name+" "+self.user.last_name

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="patient",on_delete=models.CASCADE)
    doc_d = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='doc_d', null=True)
    doc_c = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='doc_c', null=True)
    doc_p = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='doc_p', null=True)
    # def __str__(self):
    #     return self.user.first_name+" "+self.user.last_name

