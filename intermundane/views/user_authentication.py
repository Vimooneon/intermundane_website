from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

from ..forms import RegisterForm
from ..models import AccessLevel

# handles user registration, logout and profile page

# returns profile view only if user has logged in, otherwise redirects to login page
@login_required
def profile(request):
    return render(request, "intermundane/profile.html")

# registration functionality, is used over default because of custom access_level field and not requiring email field
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.access_level = AccessLevel.objects.get(level=1)
            user.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

'''
# an example of how could login functionality be implemented
# is not needed because django has a default login implementation

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        return render(request, "intermundane/login.html", {"error":"incorrect password or username"})
    return render(request, "intermundane/login.html")
'''

# logout functionality
def logout_view(request):
    logout(request)
    return redirect("index")