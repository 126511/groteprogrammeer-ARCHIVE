from django.db import models
from django.contrib.auth.models import User
from files.models import LatestPage, Filepage

# Create your models here.

class Courselist(models.Model):
    name = models.CharField(max_length=64)
    start = models.ForeignKey(Filepage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Course " + self.name + " at /" + self.start.chapterpath

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courselist, on_delete=models.CASCADE)

    def __str__(self):
        return "User " + self.user.username + " studies " + str(self.course.name)

    

class Progress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    path = models.ForeignKey(Filepage, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.course.user) + "'s progress for " + self.path.path + " of " + self.course.course.name + " is " + str(self.completed)

    class Meta:
        unique_together = ('course', 'path')

class OldProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Courselist, on_delete=models.CASCADE, null=True, blank=True)
    path = models.ForeignKey(Filepage, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + "'s progress for " + self.path.path + " of " + self.course.name + " is " + str(self.completed)





