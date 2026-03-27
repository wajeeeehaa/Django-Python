from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

# Create your models here.
class Chaivarity(models.Model):
    # enums
    CHAI_TYPE_CHOICES = [
    ('ML', 'MASALA'),
    ('GR', 'GINGER'),
    ('KL', 'KIWI'),
    ('PL', 'PLAIN'),
    ('EL', 'ELAICHI'),
    ]
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, 'Chai name must be at least 2 characters.')]
    )
    # 3rd party plugin pillow
    image = models.ImageField(upload_to="images/")
    description = models.TextField(
        validators=[MinLengthValidator(10, 'Description must be at least 10 characters.')]
    )
    type = models.CharField(max_length=2, choices=CHAI_TYPE_CHOICES, default='PL')
    data_added = models.DateTimeField(default=timezone.now)
    
    def clean(self):
        """Validate Chaivarity fields"""
        super().clean()
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Chai name cannot be empty.'})
        if not self.description or not self.description.strip():
            raise ValidationError({'description': 'Description cannot be empty.'})
        if not self.image:
            raise ValidationError({'image': 'An image is required.'})
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, 'Student name must be at least 2 characters.')]
    )
    age = models.IntegerField(
        validators=[
            MinValueValidator(5, 'Student age must be at least 5 years old.'),
            MaxValueValidator(100, 'Please enter a valid age.')
        ]
    )
    email = models.EmailField(unique=True)
    grade = models.CharField(max_length=10)
    
    def clean(self):
        """Validate Student fields"""
        super().clean()
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Student name cannot be empty.'})
        if not self.email:
            raise ValidationError({'email': 'Email address is required.'})
        if self.age and (self.age < 5 or self.age > 100):
            raise ValidationError({'age': 'Age must be between 5 and 100.'})
        if not self.grade or not self.grade.strip():
            raise ValidationError({'grade': 'Grade cannot be empty.'})
        # Check for unique email only if it's a new instance or the email has changed
        if not self.pk:  # New instance
            if Student.objects.filter(email=self.email).exists():
                raise ValidationError({'email': 'A student with this email already exists.'})
        else:  # Existing instance
            if Student.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                raise ValidationError({'email': 'A student with this email already exists.'})
    
    def __str__(self):
        return self.name