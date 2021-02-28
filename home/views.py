from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# Decide whether the default path redirects to /user or /index
def home_index(request):
    # If the user's not logged in, go to /index, otherwise to /user
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/index")
    return HttpResponseRedirect("/user")

# Render a form for the user to log in
def login_view(request):
    # Logs the user in via a form
    if request.method == "POST":
        # Cache the data provided and check the validity of the credentials
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If the user's credentials are valid
        if user is not None:
            # Log the user in and redirect to /user, unless provided an extra argument 'next'
            login(request, user)
            next = request.POST.get('next')
            if next:
               return HttpResponseRedirect(next)
            return HttpResponseRedirect("/user")
        # If the user's credentials are not valid
        else:
            # Let them try again and shout at them
            return render(request, "home/login.html", {
                "message": "That's not valid input you blithering idiot!!!!!!!",
                "status_code":-1
            })

    # Render the form for the user so they can log in
    else:
        return render(request, "home/login.html")

# Log users out
def logout_view(request):
    # Log the user out and redirect to the main page, providing a message of success
    logout(request)
    return render(request, "home/index.html", {
        "message": "We logged you out.",
        "status_code":1
    })

# General home-page
def index(request):
    # Render the corresponding template
    return render(request, "home/index.html")

# Render a page specific for a user
@login_required
def user(request):
    # Render the corresponding template, if the user's logged in
    return render(request, "home/user.html")

# Register a user
def register(request):
    # Create a form with which the user can log in
    form = UserCreationForm(request.POST)
    # If the user's provided a valid form
    if form.is_valid():
        # Save the data
        form.save()
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")
        
        # Register the user and log them in automatically
        user = authenticate(username=username, password=password1)
        login(request, user)

        # Render their own user page and a corresponding message of success
        return render(request, 'home/user.html', {
            "message":"We've created your account!",
            "status_code":1
        })
    
    else:
        # Render the template with the form
        return render(request, "home/register.html", {
            'form':form
        })