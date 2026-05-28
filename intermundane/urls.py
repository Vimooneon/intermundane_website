from django.urls import path

from . import views, user_authentication, progress

#from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("worlds", views.worlds, name="worlds"),
    path("worlds/<slug:title>", views.world_detail, name="world_detail"),
    path("characters", views.characters, name="characters"),
    path("characters/<slug:title>", views.character_detail, name="character_detail"),
    path("profile", user_authentication.profile, name="profile"),
    path("register", user_authentication.register_view, name="register_view"),

    path("logout", user_authentication.logout_view, name="logout_view"),

    path("found-code", progress.found_code, name="found_code")
]

# path("accounts/login/", auth_views.LoginView.as_view(template_name="intermundane/login.html")), path("login", user_authentication.login_view, name="login_view"),