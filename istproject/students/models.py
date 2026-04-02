from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        # ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    #custom user contains first name, last name, email, password, username
    address = models.CharField(max_length=255, blank=True, null=True)
    courses = models.ManyToManyField('Course', related_name='students', blank=True)
    
    def clean(self):
        """Validate CustomUser fields"""
        super().clean()
        if not self.first_name or not self.first_name.strip():
            raise ValidationError({'first_name': 'First name cannot be empty.'})
        if not self.last_name or not self.last_name.strip():
            raise ValidationError({'last_name': 'Last name cannot be empty.'})
        if not self.email or '@' not in self.email:
            raise ValidationError({'email': 'Please provide a valid email address.'})

class Course(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, 'Course title must be at least 3 characters.')]
    )
    description = models.TextField(
        validators=[MinLengthValidator(10, 'Description must be at least 10 characters.')]
    )
    
    def clean(self):
        """Validate Course fields"""
        super().clean()
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Course title cannot be empty.'})
        if not self.description or not self.description.strip():
            raise ValidationError({'description': 'Course description cannot be empty.'})
    
    def __str__(self):
        return self.title

 