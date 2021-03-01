from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

# Stores a file to be viewed
class Filepage(models.Model):
    # The path of its url
    chapterpath = models.CharField(max_length=16, default="h1")
    path = models.CharField(max_length=16, default="1")

    # It's title and file itself
    title = models.CharField(max_length=32, default="title")
    # This stores just text, but should be HTML code, 
    # the view and template make sure it'll be seen as HTML, not raw text
    file = models.TextField()

    def slug(self):
        return slugify(self.path), slugify(self.chapterpath)

    def __str__(self):
        return self.title + " on /" + self.chapterpath + "/" + self.path

# Saves the latest chapterpath and path a user's visited
class LatestPage(models.Model):
    # Link to the Users table Django made 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chapterpath = models.CharField(max_length=16, default="h1")
    path = models.CharField(max_length=16, default="1")

    def __str__(self):
        return str(self.user) + " has " + self.chapterpath + "/" + self.path



    


