from django.db.models.signals import post_delete
from django.conf import settings
from django.dispatch import receiver
from upload_download.models import *




@receiver(post_delete, sender=Uploaded_File)
def uploaded_file_delete(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            uploaded_file_delete(sender,instance,field,instance_file_field)