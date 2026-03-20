from django.contrib import admin

# Register your models here.
from .models import World, Character

admin.site.register(World)
admin.site.register(Character)