from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

class AccessLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    #description = models.CharField(max_length=255)
    def __str__(self):
        return self.name + " (level: "+str(self.level)+")"

class User(AbstractUser):
    email = None
    created = models.DateTimeField(auto_now_add=True, blank=True)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.username

class World(models.Model):
    title = models.CharField(max_length=255)
    #page_route = models.CharField(max_length=255, blank=True) #remove?
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title

class Character(models.Model):
    title = models.CharField(max_length=255)
    #page_route = models.CharField(max_length=255, blank=True) #remove?
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title

class ContentBlock(models.Model):
    key = models.CharField(max_length=255, unique=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        constraints = [models.CheckConstraint(check=(Q(character__isnull=False)|Q(world__isnull=False)),name="requires_character_or_world")]
    def __str__(self):
        return self.key

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.ForeignKey(ContentBlock, on_delete=models.CASCADE)
    unlocked = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'key',)
    def __str__(self):
        return self.user + " -> " + self.key

class Response(models.Model):
    user_input = models.CharField(max_length=255, unique=True)
    response = models.CharField(max_length=255, unique=True)
    action = models.CharField(max_length=255, unique=True)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, null=True, blank=True)
    content_block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user_input + " -> " + self.response + " ("+self.action+")"

class AuditLog(models.Model):
    action = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user + " -> " + self.action + " ("+str(self.timestamp)+")"

class Description(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField()
    languageCode = models.CharField(max_length=10)
    sequenceNumber = models.IntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        constraints = [models.CheckConstraint(check=(Q(character__isnull=False)|Q(world__isnull=False)),name="requires_a_character_or_world")]
    def __str__(self):
        if self.world:
            return self.title + " (world: " + self.world.title + ")" + "[" + self.languageCode + "]"
        return self.title + " (character:" + self.character.title + ")" + "[" + self.languageCode + "]"



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