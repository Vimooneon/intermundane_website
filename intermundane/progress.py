from django.shortcuts import render, redirect

from .models import Response, UserProgress, AuditLog, AccessLevel

def index(request):
    if request.method != "POST": # ==Get
        return render(request, "intermundane/index.html")

    if not request.user.is_authenticated:                                       # no account
        return render(request, "intermundane/index.html", {"error":"need-login"})

    response = Response.objects.filter(user_input = request.POST["code"].lower()).first()
    if not response:                                                            # no response exists
        return render(request, "intermundane/index.html", {"error":"no-code"})

    user_level = request.user.access_level.level
    if response.access_level and user_level < response.access_level.level:      # not enough level for response
        return render(request, "intermundane/index.html", {"error":"early-code"})

    if response.action=="redirect":
        return redirect(response.response)

    if response.action=="promote":
        if user_level == response.access_level.level:
            request.user.access_level = AccessLevel.objects.get(level=user_level+1)
            request.user.save()
            log = AuditLog(
                user=request.user,
                source="arg",
                action=response.action+" level to: "+str(response.access_level.level+1)
            )
            log.save()

    if response.action=="unlock":
        progress = UserProgress.objects.filter(user=request.user, content_key=response.content_block)
        if not progress:
            obj = UserProgress(
                user=request.user,
                content_key=response.content_block
            )
            obj.save()
            log = AuditLog(
                user=request.user,
                source="arg",
                action=response.action+" "+response.content_block.key
            )
            log.save()

    return render(request, "intermundane/index.html", {"response":response.response})