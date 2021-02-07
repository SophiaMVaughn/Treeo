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
        (2, 'Pysician'),
        (3, 'Dietician'),
        (4, 'Coach'),
        (5, 'Patient'),
    )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=5)
    is_staff = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    # phone_no = models.CharField(max_length = 10)
    # profile_pic = models.ImageField(default=profile.png, upload_to='profile_pictures')
    #objects = CustomUserManager()


# email = models.EmailField(_('email address'), unique=True)
#     email stuff piont of email adress
#
# #   USERNAME_FIELD = 'email'
# #   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
# #   def __str__(self):
# #       return "{}".format(self.email)



class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Admin'

class Physician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Physician'

class Dietician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Dietician'

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Coach'

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Patient'
