from django.contrib import admin
from .models import Course, Courselist, Progress, OldProgress

# Register your models here.
admin.site.register(Course)
admin.site.register(Courselist)
admin.site.register(Progress)
admin.site.register(OldProgress)