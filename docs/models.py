from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

# Model that stores a term
class Term(models.Model):
    # There are 3 pre-defined tags: hardware, programming in general and C
    class Tags(models.TextChoices):
        HARDWARE = "HW", "Hardware"
        PROGRAMMING = "PG", "Programming"
        C = "C", "C"

    # Storing the term,
    term = models.CharField(max_length=64)
    # its definition,
    definition = models.TextField(max_length=1024)
    # the lesson it was learned in,
    # Format: year-chapterchapter-lessonlesson, so chapter 4, lesson 2 in year 5 makes 50402
    lesson = models.BigIntegerField(default=0)
    # the tag it belongs to,
    tags = models.CharField(max_length=2, choices=Tags.choices, default=None, blank=True)
    # and its link: a slug of the title (e.g. term = "an integer" then link = "an-integer", must define yourself)
    link = models.CharField(max_length=96, default="hoii")

    # Define this model's name for the admin page
    def __str__(self):
        return str(self.term + "learned on " + str(self.lesson) + ": " + self.tags)

    # Define the slug for the link of this term
    def slug(self):
        return slugify(self.term)