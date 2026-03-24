from django.db import models
from django.db.models import Q

class AccessLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    #description = models.CharField(max_length=255)
    def __str__(self):
        return self.name + " (level:"+str(self.level)+")"

# Create your models here.
class Account(models.Model):
    user = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.user

class World(models.Model):
    title = models.CharField(max_length=255)
    page_route = models.CharField(max_length=255) #remove?
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title

class Character(models.Model):
    title = models.CharField(max_length=255)
    page_route = models.CharField(max_length=255) #remove?
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE,default=1)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class ContentBlock(models.Model):
    key = models.CharField(max_length=255, unique=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, null=True)
    class Meta:
        constraints = [models.CheckConstraint(check=(Q(character__isnull=False)|Q(world__isnull=False)),name="requires_character_or_world")]
    def __str__(self):
        return self.key

class UserProgress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    key = models.ForeignKey(ContentBlock, on_delete=models.CASCADE)
    unlocked = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'key',)

'''
guide from django documentation:

Change your models (in models.py).

Run
    python manage.py makemigrations
to create migrations for those changes

Run
    python manage.py migrate
to apply those changes to the database.


Optional: Run
    python manage.py sqlmigrate intermundane 0001
to see changes


from intermundane.models import Worlds, Characters, AccessLevel

AccessLevel.objects.create(id=1, name="Guest")

w = Worlds(title="Dark forest", page_route="")

'''