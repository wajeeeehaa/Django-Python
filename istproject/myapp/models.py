from django.db import models
from django.utils import timezone
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
    name=models.CharField(max_length=100)
    # 3rd party plugin pillow
    image=models.ImageField(upload_to="images/")
    description=models.TextField()
    type=models.CharField(max_length=2,choices=CHAI_TYPE_CHOICES,default='PL')
    data_added=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField(unique=True)
    grade=models.CharField(max_length=10)
    def __str__(self):
        return self.name