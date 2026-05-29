from django.shortcuts import get_object_or_404, render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader

from .models import World, Character, WorldContentBlock



def worlds(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level)
    world_descriptions = WorldContentBlock.objects.filter(block_type="about", world__in = world_list)
    return render(request, "intermundane/worlds.html", {"worlds": world_descriptions})

def world_detail(request, slug):
    world = get_object_or_404(World, slug=slug)
    accessLevel = world.access_level.level
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    if(accessLevel<=user_level):
        character_list = Character.objects.filter(access_level__level__lte=user_level, world=world, is_deleted=False)
        world_description = world.story_blocks.get(world=world, block_type="about")
        return render(request, "intermundane/worlds/"+slug+".html", {"world": world_description, "characters": character_list})
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})

def characters(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level, is_deleted=False)
    character_list = Character.objects.filter(access_level__level__lte=user_level, is_deleted=False)
    world_descriptions = WorldContentBlock.objects.filter(block_type="about", world__in = world_list)
    return render(request, "intermundane/characters.html", {"worlds": world_descriptions, "characters": character_list})

def character_detail(request, slug):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    character = get_object_or_404(Character, slug=slug, is_deleted=False)
    accessLevel = character.access_level.level

    character_name =  character.content_blocks.get(character=character, block_type="name")
    character_about = character.content_blocks.get(character=character, block_type="about")
    character_powers = character.content_blocks.get(character=character, block_type="powers")

    if(accessLevel<=user_level):
        return render(request, "intermundane/characters/"+slug+".html", {"name": character_name, "about": character_about, "powers": character_powers})
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})


'''
Localisation:

django-admin makemessages -l es

django-admin compilemessages

'''