from django.db import models
from django.contrib.auth.models import AbstractUser, User
# from django.utils.translation import ugettext_lazy as _
# from django.conf import settings
# from datetime import date
#
# class User(AbstractUser):
#   username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
#   email = models.EmailField(_('email address'), unique = True)
#   native_name = models.CharField(max_length = 5)
#   phone_no = models.CharField(max_length = 10)
#   profile_pic = models.ImageField(default=profile.png, upload_to='profile_pictures')
#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
#   def __str__(self):
#       return "{}".format(self.email)
#user pic?????????

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Admin'

class Pysician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Pysician'

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
