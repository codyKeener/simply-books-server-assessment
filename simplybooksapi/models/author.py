from django.db import models

class Author(models.Model):
  
  email = models.CharField(max_length=50)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  image = models.URLField()
  favorite = models.BooleanField()
  uid = models.CharField(max_length=30)
