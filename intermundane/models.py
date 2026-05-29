from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from parler.models import TranslatableModel, TranslatedFields

class AccessLevel(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255)
    )
    level = models.IntegerField(default=0)
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) + " ("+str(self.level)+")"

class User(AbstractUser):
    email = None
    created = models.DateTimeField(auto_now_add=True, blank=True)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.username

class World(models.Model):
    slug = models.CharField(max_length=255) #page_route/"title"
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.slug

class Character(models.Model):
    slug = models.CharField(max_length=255) #page_route/"title"
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, default=1)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.slug

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
    content_key = models.ForeignKey(ContentBlock, on_delete=models.CASCADE)
    unlocked = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'content_key',)
    def __str__(self):
        return self.user.username + " -> " + self.content_key.key

class Response(TranslatableModel):
    ACTION_TYPES = [
        ("say", "Say"),
        ("redirect", "Redirect"),
        ("promote", "Promote"),
        ("unlock", "Unlock"),
    ]
    user_input = models.CharField(max_length=255, unique=True)
    translations = TranslatedFields(
        response = models.CharField(max_length=255)
    )
    action = models.CharField(max_length=255, choices=ACTION_TYPES)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, null=True, blank=True)
    content_block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user_input + " -> " + self.safe_translation_getter('response', any_language=True) + " ("+self.action+")"


class AuditLog(models.Model):
    SOURCE_TYPES = [
        ("arg", "ARG"),
        ("admin panel", "Admin panel"),
    ]
    action = models.CharField(max_length=255)
    source = models.CharField(max_length=255, choices=SOURCE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " -> " + self.action + " ("+str(self.timestamp)+")"

class CharacterContentBlock(TranslatableModel):
    BLOCK_TYPES = [
        ("name", "Name"),
        ("about", "About"),
        ("powers", "Powers"),
    ]
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="content_blocks"
    )
    block_type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPES
    )
    content_key = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sequence = models.IntegerField(default=0)
    required_access_level = models.IntegerField(default=0)
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        desc=models.TextField()
    )
    class Meta:
        ordering = ["sequence"]



class WorldContentBlock(TranslatableModel):
    BLOCK_TYPES = [
        ("about", "About"),
        ("chapter", "Chapter"),
    ]

    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="story_blocks"
    )
    content_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    block_type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPES,
        default="about"
    )
    sequence = models.IntegerField(default=0)
    required_access_level = models.IntegerField(default=0)
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        desc=models.TextField()
    )
    class Meta:
        ordering = ["sequence"]

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