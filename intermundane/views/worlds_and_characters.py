from django.shortcuts import get_object_or_404, render
from django.db.models import Q

# django views correlate to the controller class in MVC pattern, meanwhile the MVC views are stored as templates

from ..models import World, Character, WorldContentBlock, UserProgress

# general worlds page navigated from navbar
def worlds(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level, is_deleted=False)
    world_descriptions = WorldContentBlock.objects.filter(block_type="about", world__in = world_list)
    return render(request, "intermundane/worlds/worlds.html", {"worlds": world_descriptions})

# specific world page navigated from worlds page
def world_detail(request, slug):
    world = get_object_or_404(World, slug=slug)
    accessLevel = world.access_level.level
    user_level=0
    user_keys = []
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
        user_keys = UserProgress.objects.filter(user=request.user).values_list("content_key_id",flat=True)
    if(accessLevel<=user_level):
        character_list = Character.objects.filter(access_level__level__lte=user_level, world=world, is_deleted=False)
        world_description = world.story_blocks.get(world=world, block_type="about")
        world_title = world.story_blocks.filter(world=world, block_type="title", access_level__level__lte=user_level).first()
        world_lore = world.story_blocks.filter(world=world, block_type="chapter").filter(Q(access_level__level__lte=user_level, unlock_type="gte") | Q(access_level__level=user_level, unlock_type="e") | Q(access_level__level__gt=user_level, unlock_type="lt") | Q(content_block__in=user_keys)).order_by('sequence')
        return render(request, "intermundane/worlds/world_template.html", {"world": world_description, "title":world_title, "characters": character_list, "lore":world_lore})
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})

# general characters page navigated from navbar
def characters(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level, is_deleted=False)
    character_list = Character.objects.filter(access_level__level__lte=user_level, is_deleted=False)
    world_descriptions = WorldContentBlock.objects.filter(block_type="about", world__in = world_list)
    return render(request, "intermundane/characters/characters.html", {"worlds": world_descriptions, "characters": character_list})

# specific character page navigated from characters page
def character_detail(request, slug):
    character = get_object_or_404(Character, slug=slug, is_deleted=False)
    accessLevel = character.access_level.level
    user_level=0
    user_keys = []
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
        user_keys = UserProgress.objects.filter(user=request.user).values_list("content_key_id",flat=True)

    character_name =  character.story_blocks.get(character=character, block_type="name")
    youtube_chibi = character.story_blocks.get(character=character, block_type="youtube")
    character_lore = character.story_blocks.filter(character=character, block_type="chapter").filter(Q(access_level__level__lte=user_level, unlock_type="gte") | Q(access_level__level=user_level, unlock_type="e") | Q(access_level__level__gt=user_level, unlock_type="lt") | Q(content_block__in=user_keys)).order_by('sequence')

    if(accessLevel<=user_level):
        return render(request, "intermundane/characters/character_template.html", {"name": character_name, "lore":character_lore, "youtube":youtube_chibi})
    return render(request, "404.html", {"error": "no-access-level"})


'''
Localisation:

create new list of messages that need translation:
django-admin makemessages -l es

make the updated translations appear on the website:
django-admin compilemessages

'''