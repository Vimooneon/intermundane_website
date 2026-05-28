from django.shortcuts import render

from .models import Response

def found_code(request):
    if request.method != "POST":
        return
    if not request.user.is_authenticated:
        return render(request, "intermundane/index.html", {"error":"need-login"})

    #user_level = request.user.access_level.level
    response = Response.objects.filter(user_input = request.POST["code"]).first()
    if not response:
        return render(request, "intermundane/index.html", {"error":"no-code"})
    if response.action=="promote":
        user_level = request.user.access_level.level
        if user_level == response.access_level.level-1:
            request.user.access_level = response.access_level
            request.user.save()
        elif user_level < response.access_level.level-1:
             return render(request, "intermundane/index.html", {"error":"early-code"})
    return render(request, "intermundane/index.html", {"response":response.response})