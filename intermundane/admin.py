from django.contrib import admin

# Register your models here.
from .models import World, Character, AccessLevel, User, ContentBlock, UserProgress, Response, AuditLog, Description

admin.site.register(World)
admin.site.register(Character)
admin.site.register(AccessLevel)
admin.site.register(User)
admin.site.register(ContentBlock)
admin.site.register(UserProgress)
admin.site.register(Response)
admin.site.register(AuditLog)
admin.site.register(Description)