from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Rating(models.Model):
    score = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__type':'TRAINER'})
    count = models.IntegerField(default=0)

class Contact(models.Model):
    phone = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__type':'TRAINER'})