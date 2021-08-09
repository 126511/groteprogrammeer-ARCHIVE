from django.contrib import admin
from .models import Term

# Import the models from models.py into the admin page
admin.site.register(Term)

