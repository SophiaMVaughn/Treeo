from django.db import models

class PostQ(models.Model):
    Name= models.CharField(max_length=200)
    Message=models.CharField(max_length=200)


