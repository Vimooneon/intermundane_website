from django.db import models

# Create your models here.
class Account(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created = models.DateTimeField()
    access_level = models.IntegerField(default=0)
    def __str__(self):
        return self.user

class World(models.Model):
    title = models.CharField(max_length=255)
    page_route = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class Character(models.Model):
    title = models.CharField(max_length=255)
    page_route = models.CharField(max_length=255)
    access_level = models.IntegerField(default=0)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    def __str__(self):
        return self.title


'''
guide from django documentation:

Change your models (in models.py).

Run
    python manage.py makemigrations
to create migrations for those changes


Run
    python manage.py sqlmigrate intermundane 0001
to see changes

Run
    python manage.py migrate
to apply those changes to the database.

from intermundane.models import Worlds, Characters

w = Worlds(title="Dark forest", page_route="")

'''