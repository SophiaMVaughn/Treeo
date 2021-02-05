from django.contrib import admin
from .models import Todo
# , Profile

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    

# class ProfileAdmin(admin.ModelAdmin):
#     # readonly_fields = ('email_confirmed',)
#     pass
# Register your models here.
admin.site.register(Todo, TodoAdmin)
# admin.site.register(Profile, ProfileAdmin)
