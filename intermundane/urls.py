from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("worlds", views.worlds, name="worlds"),
    path("worlds/<slug:title>", views.world_detail, name="world_detail"),
    path("characters", views.characters, name="characters"),
    path("characters/<slug:title>", views.character_detail, name="character_detail"),
    path("profile", views.profile, name="profile"),
    path("registration", views.registration, name="registration"),
    path("login", views.login, name="login"),
]