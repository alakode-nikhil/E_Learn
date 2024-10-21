from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'profile__type':'TRAINER'})
    price = models.IntegerField()
    is_rated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '{}'.format(self.course_name)

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=100)
    chapter_video = models.FileField(upload_to='course_videos/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{}'.format(self.chapter_name)

class ChapterCompleted(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '{}'.format(self.chapter_name)
    
class ChapterRating(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    chapter_rating = models.IntegerField(default=0)
    count = models.IntegerField(default=0)