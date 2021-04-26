from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
#from .managers import CustomUserManager
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
import uuid

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
Survey_TYPE_CHOICES = (
    (1, 'Not Taken'),
    (2, 'Taken'),
    (3, 'Refused'),
)

class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=3)
    is_staff = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    phone_no = PhoneNumberField(null=True, blank=True, unique=True)
    profile_pic = models.ImageField(
        default='img/profile.png', upload_to='profile_pictures')
    ota_wait = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # this is using a pillow package might be resource heavy on server side alternatives???
        # also might run this check every login??????
        super().save()
        temp = Image.open(self.profile_pic.path)
        if temp.height > 200 or temp.height > 200:
            temp.thumbnail((200, 200))
            temp.save(self.profile_pic.path)

    #objects = CustomUserManager()
# #   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

# acess via
# provider.user.last_name.
# user.related profile name.Patient_count
#object.get_chices_display

class Admin(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="admin", on_delete=models.CASCADE)


class Provider(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="provider", on_delete=models.CASCADE)
    Patient_count = models.PositiveSmallIntegerField(default=0)
    Provider_type = models.PositiveSmallIntegerField(
        choices=PROVIDER_TYPE_CHOICES, default=1)
    is_verified = models.BooleanField(default=False)


class Patient(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="patient", on_delete=models.CASCADE)
    doc_d = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='doc_d', null=True)
    doc_c = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='doc_c', null=True)
    doc_p = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='doc_p', null=True)
    survey_status=models.PositiveSmallIntegerField(
        choices=Survey_TYPE_CHOICES, default=1)
    survey_info=models.CharField(max_length=20,null=True)
