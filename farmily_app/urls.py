from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("profile/<int:pk>/product<int:prpk>/edit", views.profile_edit, name="profile-edit"),
    path("profile/<int:pk>/create", views.profile_create, name="profile-create"),
]

