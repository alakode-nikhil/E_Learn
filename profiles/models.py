from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    USER_TYPES = [
        ('STUDENT','student'),
        ('TRAINER','trainer'),
        ('MANAGER','manager')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10,choices=USER_TYPES)
    country = models.CharField(max_length=100, default='Country')
    state = models.CharField(max_length=100, default='State')
    district = models.CharField(max_length=100, default='District')