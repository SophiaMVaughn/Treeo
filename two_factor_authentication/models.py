import logging
from binascii import unhexlify
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_otp.models import Device, ThrottlingMixin
from django_otp.oath import totp
from phonenumber_field.modelfields import PhoneNumberField
import logging
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_str
from django_otp.models import SideChannelDevice, ThrottlingMixin



logger = logging.getLogger(__name__)




class PhoneDevice(ThrottlingMixin, SideChannelDevice):
    #this might need to be unique since you probably dont want  one phone on multiple accounts
    number = PhoneNumberField()

    class Meta(SideChannelDevice.Meta):
        verbose_name = "Phone Device"

    # def generate_challenge_sms(self, secs):


    # def send_token(self, token):


