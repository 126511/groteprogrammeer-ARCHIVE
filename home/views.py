from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_index(request):
    # Decides whether the default path ("") redirects to /user or /index
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/index")
    return HttpResponseRedirect("/user")

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
                "message": "That's not valid input you blithering idiot!!!!!!!"
            })

    # Render the form for the user so they can log in
    else:
        return render(request, "home/login.html")


def logout_view(request):
    # Log the user out and redirect to the main page, providing a message of success
    logout(request)
    return render(request, "home/index.html", {
        "message": "We logged you out."
    })

def index(request):
    # Render the corresponding template
    return render(request, "home/index.html")

@login_required
def user(request):
    # Render the corresponding template, if the user's logged in
    return render(request, "home/user.html")






