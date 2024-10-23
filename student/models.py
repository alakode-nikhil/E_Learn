from django.db import models
from manager.models import Course, Chapter
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class IsPurchased(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)

class CanRate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    can_rate = models.BooleanField(default=True)
    
class CanRateChapter(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    can_rate = models.BooleanField(default=True)

class FeedBack(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(default="")

class PaymentDetails(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=25, default='Card')
    payment_date = models.DateField(default=timezone.now)
    payment_amount = models.IntegerField(default = 0)