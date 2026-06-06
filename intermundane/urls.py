from django.urls import path

from . import views, user_authentication, progress, admin_panel

# links url paths to django views

urlpatterns = [
    path("", progress.index, name="index"),

    path("worlds", views.worlds, name="worlds"),
    path("worlds/<slug:slug>", views.world_detail, name="world_detail"),
    path("characters", views.characters, name="characters"),
    path("characters/<slug:slug>", views.character_detail, name="character_detail"),

    path("profile", user_authentication.profile, name="profile"),
    path("accounts/register", user_authentication.register_view, name="register_view"),
    path("logout", user_authentication.logout_view, name="logout_view"),

    path("admin_panel", admin_panel.panel, name="admin_panel"),
    path("set_level", admin_panel.set_level, name="set_level"),
    path("add_key", admin_panel.add_key, name="add_key"),
    path("remove_key", admin_panel.remove_key, name="remove_key"),
    path("ban_user", admin_panel.ban_user, name="ban_user"),
]

#   path("login", user_authentication.login_view, name="login_view"), is unused because of django default login view - auth_views.LoginView