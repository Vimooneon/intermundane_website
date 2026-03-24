from django.contrib import admin

# Register your models here.
from .models import World, Character, AccessLevel, Account, ContentBlock

admin.site.register(World)
admin.site.register(Character)
admin.site.register(AccessLevel)
admin.site.register(Account)
admin.site.register(ContentBlock)