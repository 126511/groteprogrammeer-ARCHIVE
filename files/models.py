from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

# Stores a file to be viewed
class Filepage(models.Model):
    # The path of its url
    chapterpath = models.CharField(max_length=16, default="h1", null=True, blank=True)
    path = models.CharField(max_length=16, default="1")

    # It's title and file itself
    title = models.CharField(max_length=32, default="title")
    # This stores just text, but should be HTML code, 
    # the view and template make sure it'll be seen as HTML, not raw text
    file = RichTextField()

    def slug(self):
        return slugify(self.path), slugify(self.chapterpath)

    def __str__(self):
        return self.title + " on /" + self.chapterpath + "/" + self.path
    
    class Meta:
        ordering = ['chapterpath', 'path']

# Saves the latest chapterpath and path a user's visited
class LatestPage(models.Model):
    # Link to the Users table Django made 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filepage = models.ForeignKey(Filepage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user) + " has " + str(self.filepage)


    


