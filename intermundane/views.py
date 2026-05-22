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
    world_list = World.objects.filter(access_level__level=0)
    return render(request, "intermundane/worlds.html", {"worlds": world_list})

def world_detail(request, title):
    world = get_object_or_404(World, title=title)
    accessLevel = world.access_level.level
    if(accessLevel==0):
        return render(request, "intermundane/worlds/"+title+".html")
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})


def characters(request):
    world_list = World.objects.filter(access_level__level=0)
    character_list = Character.objects.filter(access_level__level=0)
    return render(request, "intermundane/characters.html", {"worlds": world_list, "characters": character_list})

def character_detail(request, title):
    character = get_object_or_404(Character, title=title)
    accessLevel = character.access_level.level
    if(accessLevel==0):
        return render(request, "intermundane/characters/"+title+".html")
    return render(request, "intermundane/no-such-page.html", {"error": "you dont have necessary permission level"})

def profile(request):
    return render(request, "intermundane/characters.html")

def registration(request):
    return render(request, "intermundane/characters.html")

def login(request):
    return render(request, "intermundane/characters.html")