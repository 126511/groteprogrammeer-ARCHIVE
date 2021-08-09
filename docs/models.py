from django.db import models
from django.template.defaultfilters import slugify
from files.models import Filepage

# Create your models here.
class Term(models.Model):
    class Tags(models.TextChoices):
        HARDWARE = "HW", "Hardware"
        PROGRAMMING = "PG", "Programming"
        C = "C", "C"

    term = models.CharField(max_length=64)
    definition = models.TextField(max_length=1024)
    lesson = models.ForeignKey(Filepage, on_delete=models.PROTECT)
    tags = models.CharField(max_length=2, choices=Tags.choices, default=None, blank=True)
    link = models.CharField(max_length=96)

    def __str__(self):
        return str(self.term + " learned on " + str(self.lesson) + ": " + self.tags)

    def slug(self):
        return slugify(self.term)