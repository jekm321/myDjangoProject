from django.contrib import admin
from .models import Note
from .models import PersonalNote

# Register your models here.

admin.site.register(Note)
admin.site.register(PersonalNote)