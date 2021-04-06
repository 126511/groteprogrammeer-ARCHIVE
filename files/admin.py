from django.contrib import admin
from .models import Filepage, LatestPage, Term

# Register your models here.
admin.site.register(Filepage)
admin.site.register(LatestPage)
admin.site.register(Term)