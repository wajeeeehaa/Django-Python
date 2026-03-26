from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    #custom user contains first name, last name, email, password, username
    address= models.CharField(max_length=255, blank=True, null=True)
    