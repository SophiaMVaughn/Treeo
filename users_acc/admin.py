from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Admin)
admin.site.register(Pysician)
admin.site.register(Dietician)
admin.site.register(Coach)
admin.site.register(Patient)