from django.db import models

class PostQ(models.Model):
    Name = models.CharField(default=0,max_length=200)
    Message = models.CharField(max_length=200)
