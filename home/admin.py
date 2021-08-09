from django.contrib import admin
from .models import Course, Courselist, Progress, OldProgress, Teachers

# Import the models from models.py into the admin page
admin.site.register(Course)
admin.site.register(Courselist)
admin.site.register(Progress)
admin.site.register(OldProgress)
admin.site.register(Teachers)