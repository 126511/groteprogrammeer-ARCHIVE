from django.db import models
from django.contrib.auth.models import User
from files.models import LatestPage, Filepage

# Create your models here.

# Model lists all courses
class Courselist(models.Model):
    # Storing their name (e.g. Chapter 1)
    name = models.CharField(max_length=64)
    # and their starting page (e.g. Paragraph 1)
    start = models.ForeignKey(Filepage, on_delete=models.CASCADE, null=True, blank=True)

    # Define this model's name for the admin page
    def __str__(self):
        return "Course " + self.name + " at /" + self.start.chapterpath

# Model that combines a course with a user
class Course(models.Model):
    # Storing the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # and their course
    course = models.ForeignKey(Courselist, on_delete=models.CASCADE)

    # Define this model's name for the admin page
    def __str__(self):
        return "User " + self.user.username + " studies " + str(self.course.name)

# Model that stores the user's current progress
class Progress(models.Model):
    # Storing their course,
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # the page of the progress were saving
    path = models.ForeignKey(Filepage, on_delete=models.CASCADE)
    # and whether it's completed or not
    completed = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        return str(self.course.user) + "'s progress for " + self.path.path + " of " + self.course.course.name + " is " + str(self.completed)

    # Make sure the same course and path can never be together: a user can never have 2 progresses for the same page
    class Meta:
        unique_together = ('course', 'path')

# Model that stores progress of courses user are not currently signed in to
class OldProgress(models.Model):
    # Storing the user,
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # the course it belongs to
    course = models.ForeignKey(Courselist, on_delete=models.CASCADE, null=True, blank=True)
    # the page it belongs to
    path = models.ForeignKey(Filepage, on_delete=models.CASCADE, null=True, blank=True)
    # and whether it's completed
    completed = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        return str(self.user) + "'s progress for " + self.path.path + " of " + self.course.name + " is " + str(self.completed)

# Model that stores what users are teachers
class Teachers(models.Model):
    # Storing the user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # and a bool whether they're teacher
    teacher = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        if self.teacher:
            return str(self.user) + " is a teacher"
        else:
            return str(self.user) + " is a student"

