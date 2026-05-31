from django.contrib import admin
from parler.admin import TranslatableAdmin

# Register your models here.
from .models import World, Character, User, ContentBlock, UserProgress, AuditLog, CharacterContentBlock, WorldContentBlock, AccessLevel, Response

admin.site.register(World)
admin.site.register(Character)
admin.site.register(User)
admin.site.register(ContentBlock)
admin.site.register(UserProgress)
admin.site.register(AuditLog)

@admin.register(CharacterContentBlock)
class CharacterContentBlockAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "character",
        "block_type",
        "title",
        "sequence",
    )
    search_fields = (
        "translations__title",
        "translations__body",
    )

@admin.register(AccessLevel)
class AccessLevelTranslatedAdmin(TranslatableAdmin):
    list_display = (
        "level",
    )
    search_fields = (
        "translations__name",
    )

@admin.register(Response)
class ResponseTranslatedAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "user_input",
        "action",
        "is_deleted",
    )
    search_fields = (
        "translations__response",
    )

@admin.register(WorldContentBlock)
class WorldContentBlockAdmin(TranslatableAdmin):

    list_display = (
        "id",
        "world",
        "title",
        "sequence",
    )

    search_fields = (
        "translations__title",
        "translations__body",
    )
