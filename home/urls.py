from django.urls import path, include
from . import views

# Define all urls for the home webapp
urlpatterns = [
    # No template, decides whether a user should see the "index" or "user" page
    path("", views.home_index, name="home_index"),
    # Page where users can log in into their accounts
    path("login", views.login_view, name="login"),
    # Page where users can log out of their accounts
    path("logout", views.logout_view, name="logout"),
    # Page for all visitor of the site, even those without an account
    path("index", views.index, name="main_index"),
    # Homepage for all users
    path("user", views.user, name="user"),
    # Homepage for all teachers, only visible if they are a teacher
    path("teacher", views.teacher, name="teacher"),
    # Page where users can sign up for a free account
    path("register", views.register, name="register"),
    # No template, gets the progress data from the database
    path("progress", views.progress, name="progress"),
    # No template, deletes a student from a current course
    path("leavecourse", views.leavecourse, name="leavecourse"),
    # Page that tells about us
    path("about-us", views.about_us, name="about-us"),
    # PAge that tells about the school thesis
    path("pws", views.pws, name="pws"),
    # Page that holds contact information
    path("contact", views.contact, name="contact"),

    path('accounts/', include('allauth.urls')),
]