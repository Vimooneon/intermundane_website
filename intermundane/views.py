from django.shortcuts import get_object_or_404, render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader

from .models import World, Character

def index(request):
    return render(request, "intermundane/index.html")

    #template = loader.get_template("intermundane/intermundane.html")
    #return HttpResponse(template.render())

def worlds(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level)
    return render(request, "intermundane/worlds.html", {"worlds": world_list})

def world_detail(request, title):
    world = get_object_or_404(World, title=title)
    accessLevel = world.access_level.level
    if(accessLevel==0):
        return render(request, "intermundane/worlds/"+title+".html")
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})


def characters(request):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    world_list = World.objects.filter(access_level__level__lte=user_level)
    character_list = Character.objects.filter(access_level__level__lte=user_level)
    return render(request, "intermundane/characters.html", {"worlds": world_list, "characters": character_list})

def character_detail(request, title):
    user_level=0
    if request.user.is_authenticated:
        user_level = request.user.access_level.level
    character = get_object_or_404(Character, title=title)
    accessLevel = character.access_level.level
    if(accessLevel<=user_level):
        return render(request, "intermundane/characters/"+title+".html")
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})


'''
Localisation:

django-admin makemessages -l es

django-admin compilemessages

'''