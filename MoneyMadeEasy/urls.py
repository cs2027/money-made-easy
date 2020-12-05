from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login_page", views.login_page, name="login"),
    path("logout_page", views.logout_page, name="logout")
]