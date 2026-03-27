from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Create your models here.
class CustomUser(AbstractUser):
    #custom user contains first name, last name, email, password, username
    address = models.CharField(max_length=255, blank=True, null=True)
    
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

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # OneToOneField is exactly how we link a student profile to a single authentication account,
    # and ForeignKey is the perfect "ticket" for a One-to-Many relationship.
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    
    def clean(self):
        """Validate Student fields"""
        super().clean()
        if not self.user:
            raise ValidationError({'user': 'A student must be associated with a user account.'})
    
    def __str__(self):
        return self.user.username