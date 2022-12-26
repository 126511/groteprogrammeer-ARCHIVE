from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

# Stores a file to be viewed
class Lesson(models.Model):
    # The path of its url
    chapterpath = models.CharField(max_length=16)
    path = models.CharField(max_length=128)

    # It's title and file itself
    title = models.CharField(max_length=128)
    # This stores just text, but should be HTML code, 
    # the view and template make sure it'll be seen as HTML, not raw text
    file = models.TextField()

    def slug(self):
        return slugify(self.path), slugify(self.chapterpath)

    def __str__(self):
        return self.title + " on /" + self.chapterpath + "/" + self.path
    
    class Meta:
        ordering = ['chapterpath', 'path']

# Saves the latest chapterpath and path a user's visited
class LatestVisit(models.Model):
    # Link to the Users table Django made 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " has visited " + self.lesson.title + " last"


    


