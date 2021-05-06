from django.contrib import admin
from django.apps import AppConfig
from .models import *

# Register your models here.
class two_factor_authConfig(AppConfig):
    name = 'two_factor_auth'
admin.site.register(PhoneDevice)
# admin.site.register(User, UserAdmin)
# admin.site.register(Provider)
# admin.site.register(Patient)
