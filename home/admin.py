from django.contrib import admin
from .models import *

# Import the models from models.py into the admin page
admin.site.register(Chapter)
admin.site.register(UserToChapter)
admin.site.register(Progress)
admin.site.register(OldProgress)
admin.site.register(Teacher)