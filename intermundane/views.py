from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader

from .models import World, Character, Description

def index(request):
    return render(request, "intermundane/index.html")

    #template = loader.get_template("intermundane/intermundane.html")
    #return HttpResponse(template.render())

def worlds(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level)
    language = get_language()
    world_descriptions = Description.objects.filter(sequenceNumber=0, languageCode=language, world__in = world_list)
    if not world_descriptions:
        world_descriptions = Description.objects.filter(sequenceNumber=0, languageCode="en", world__in = world_list)
    return render(request, "intermundane/worlds.html", {"worlds": world_descriptions})

def world_detail(request, title):
    language = get_language()
    world = get_object_or_404(World, title=title)
    accessLevel = world.access_level.level
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    if(accessLevel<=user_level):
        character_list = Character.objects.filter(access_level__level__lte=user_level, world=world)
        world_description = Description.objects.get(world=world, sequenceNumber=0, languageCode=language)
        if not world_description:
            world_description = Description.objects.get(world=world, sequenceNumber=0, languageCode="en")
        return render(request, "intermundane/worlds/"+title+".html", {"world": world_description, "characters": character_list})
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})

def characters(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level)
    character_list = Character.objects.filter(access_level__level__lte=user_level)
    language = get_language()
    world_descriptions = Description.objects.filter(sequenceNumber=0, languageCode=language, world__in = world_list)
    if not world_descriptions:
        world_descriptions = Description.objects.filter(sequenceNumber=0, languageCode="en", world__in = world_list)
    return render(request, "intermundane/characters.html", {"worlds": world_descriptions, "characters": character_list})

def character_detail(request, title):
    language = get_language()
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    character = get_object_or_404(Character, title=title)
    accessLevel = character.access_level.level
    character_name =  Description.objects.get(character=character, sequenceNumber=0, languageCode=language)
    character_about = Description.objects.get(character=character, sequenceNumber=1, languageCode=language)
    character_powers = Description.objects.get(character=character, sequenceNumber=2, languageCode=language)
    if not character_name:
        character_name = Description.objects.get(character=character, sequenceNumber=0, languageCode="en")
    if not character_about:
        character_about = Description.objects.get(character=character, sequenceNumber=1, languageCode="en")
    if not character_powers:
        character_powers = Description.objects.get(character=character, sequenceNumber=1, languageCode="en")

    if(accessLevel<=user_level):
        return render(request, "intermundane/characters/"+title+".html", {"name": character_name, "about": character_about, "powers": character_powers})
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})


'''
Localisation:

django-admin makemessages -l es

django-admin compilemessages

'''