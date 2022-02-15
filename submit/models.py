from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Input(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.JSONField()
    slug = models.CharField(max_length=256)

    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.user) + "'s input for " + self.slug + " at " + str(self.datetime)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=256)

    total_tests = models.IntegerField()
    passed_tests = models.IntegerField()

    def __str__(self):
        return str(self.user) + "'s score for " + self.slug + " is " + str(self.passed_tests) + "/" + str(self.total_tests)

class File(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    file = models.TextField()

    def __str__(self):
        return self.name + " for " + str(self.input)

class Key(models.Model):
    key = models.CharField(max_length=64)
    when_requested = models.DateTimeField()

    def __str__(self):
        return self.key + " requested at " + str(self.when_requested)