from django.db import models
from django.contrib.auth.models import User
from files.models import LatestPage

# Create your models here.

class Courselist(models.Model):
    name = models.CharField(max_length=64)
    chapterpath = models.CharField(max_length=32)
    starterpath = models.CharField(max_length=32, default="1")

    def __str__(self):
        return "Course " + self.name + " at /" + self.chapterpath

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courselist, on_delete=models.CASCADE)

    def __str__(self):
        return "User " + self.user.username + " studies " + str(self.course.name)






