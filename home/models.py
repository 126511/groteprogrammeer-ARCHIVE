from django.db import models
from django.contrib.auth.models import User
from files.models import Lesson

# Create your models here.

# Model that stores the name and chapterpath of each chapter
class Chapter(models.Model):
    # Storing their name (e.g. Chapter 1)
    name = models.CharField(max_length=64)
    # and their chapterpath (e.g. h1)
    path = models.CharField(max_length=64)

    # Define this model's name for the admin page
    def __str__(self):
        return "Chapter " + self.name + " at /" + self.path

# Model that combines a course with a user
class UserToChapter(models.Model):
    # Storing the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # and their course
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    # Define this model's name for the admin page
    def __str__(self):
        return "User " + self.user.username + " studies " + self.chapter.name

# Model that stores the user's current progress
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        return self.user.username + "'s progress for " + self.lesson.title + " is " + str(self.completed)

# Model that stores progress of courses user are not currently signed in to
class OldProgress(models.Model):
    # Storing the user,
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    completed = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        return self.user.username + "'s progress for " + self.lesson.title + " is " + str(self.completed)

# Model that stores what users are teachers
class Teacher(models.Model):
    # Storing the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # and a bool whether they're teacher
    teacher = models.BooleanField(default=False)

    # Define this model's name for the admin page
    def __str__(self):
        if self.teacher:
            return self.user.username + " is a teacher"
        else:
            return self.user.username + " is a student"

