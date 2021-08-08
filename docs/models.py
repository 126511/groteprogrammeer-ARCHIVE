from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class Term(models.Model):
    class Tags(models.TextChoices):
        HARDWARE = "HW", "Hardware"
        PROGRAMMING = "PG", "Programming"
        C = "C", "C"

    term = models.CharField(max_length=64)
    definition = models.TextField(max_length=1024)
    # Format: year-chapterchapter-lessonlesson, so chapter 4, lesson 2 in year 5 makes 50402
    lesson = models.BigIntegerField(default=0)
    tags = models.CharField(max_length=2, choices=Tags.choices, default=None, blank=True)
    link = models.CharField(max_length=96)

    def __str__(self):
        return str(self.term + "learned on " + str(self.lesson) + ": " + self.tags)

    def slug(self):
        return slugify(self.term)