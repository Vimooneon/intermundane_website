from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import User, AuditLog, AccessLevel, UserProgress, ContentBlock


@login_required
def panel(request):
    if not request.user.is_staff:
        return redirect("index")
    logs = AuditLog.objects.all().order_by('-timestamp') #.reverse() #.order_by('timestamp')
    users = User.objects.all()
    levels = AccessLevel.objects.all()
    progress = UserProgress.objects.all()
    keys = ContentBlock.objects.all()
    return render(request, "intermundane/admin_panel.html", {"logs": logs, "users": users, "levels": levels, "progress": progress, "keys": keys})

def set_level(request):
    if not request.user.is_staff:
        return redirect("index")
    if request.method == "POST":
        userm = request.POST["userm"]
        level = request.POST["level"]
        actual_user=User.objects.get(username=userm)
        if not (actual_user == request.user or request.user.is_superuser):
            return redirect('admin_panel')
        actual_user.access_level = AccessLevel.objects.get(level=level)
        actual_user.save()
        log = AuditLog(
            user=request.user,
            source="admin panel",
            action=userm+" set level to:"+level
        )
        log.save()
    return redirect('admin_panel')


def remove_key(request):
    if not request.user.is_staff:
        return redirect("index")
    if request.method == "POST":
        userm = request.POST["userm"]
        content_key = request.POST["content_key"]
        actual_user = User.objects.get(username=userm)
        if not (actual_user == request.user or request.user.is_superuser):
            return redirect('admin_panel')
        actual_key = ContentBlock.objects.get(key=content_key)
        progress = UserProgress.objects.get(user=actual_user, content_key=actual_key)
        progress.delete()
        log = AuditLog(
            user=request.user,
            source="admin panel",
            action=userm+" delete unlock:"+content_key
        )
        log.save()
        return redirect('admin_panel')
    return redirect('admin_panel')

def add_key(request):
    if not request.user.is_staff:
        return redirect("index")
    if request.method == "POST":
        userm = request.POST["userm"]
        content_key = request.POST["content_key"]
        actual_user = User.objects.get(username=userm)
        if not (actual_user == request.user or request.user.is_superuser):
            return redirect('admin_panel')
        actual_key = ContentBlock.objects.get(key=content_key)
        obj = UserProgress(
            user=actual_user,
            content_key=actual_key
        )
        obj.save()
        log = AuditLog(
            user=request.user,
            source="admin panel",
            action=userm+" add unlock:"+content_key
        )
        log.save()
    return redirect('admin_panel')

def ban_user(request): #also unban user
    if not request.user.is_staff:
        return redirect("index")
    if request.method == "POST":
        userm = request.POST["userm"]
        active = request.POST["is_active"]
        actual_user = User.objects.get(username=userm)
        if actual_user != request.user and not actual_user.is_superuser:
            actual_user.is_active=active
            actual_user.save()
            log = AuditLog(
                user=request.user,
                source="admin panel",
                action=userm+" set active:"+str(active)
            )
            log.save()
    return redirect('admin_panel')