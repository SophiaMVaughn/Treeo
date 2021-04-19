from django.db import models
from django.conf import settings
import uuid
# Create your models here.
FILE_TYPE_CHOICES = (
    (1, 'Certificate'),
    (2, 'License '),
    (3, 'Other'),
)
class Uploaded_File(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usern = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #how long is max file name and is this the best way to store as var char has to aloctate 100 everytime
    file_name = models.CharField(max_length = 100)
    file = models.FileField(upload_to='uploaded_files')
    file_type=models.PositiveSmallIntegerField(choices=FILE_TYPE_CHOICES, default=3)
    #make read only
    date_created = models.DateTimeField(auto_now_add=True)