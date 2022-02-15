from django.contrib import admin
from .models import Input, Score, File, Key

# Register your models here.
admin.site.register(Input)
admin.site.register(Score)
admin.site.register(File)
admin.site.register(Key)