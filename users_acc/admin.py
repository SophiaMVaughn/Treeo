from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Physician)
admin.site.register(Dietician)
admin.site.register(Coach)
admin.site.register(Patient)