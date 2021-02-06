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
    # if you cant have more than one role
    # USER_TYPE_OPTIONS = ((1, 'patient'),(2, 'dietician'),(3, 'coach'),(4, 'physician'),(5, 'admin'),)
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
#   def __str__(self):
#       return "{}".format(self.email)
#user pic?????????

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
