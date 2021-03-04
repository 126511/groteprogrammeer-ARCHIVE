from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_index, name="home_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("index", views.index, name="index"),
    path("user", views.user, name="user"),
    path("register", views.register, name="register"),
    path("about-us", views.about_us, name="about-us"),
    path("pws", views.pws, name="pws"),
    path("contact", views.contact, name="contact")
]