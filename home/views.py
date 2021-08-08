from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Courselist, Progress, OldProgress
from files.models import Filepage

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
                "message": "Deze gegevens kloppen niet, probeer het nog een keer",
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
        "message": "Je bent nu uitgelogd",
        "status_code":1
    })

# General home-page
def index(request):
    # Render the corresponding template
    return render(request, "home/index.html")

# Render a page specific for a user, where they can jump back into their course, or sign up for one
@login_required
def user(request):
    try:
        message = request.session['message']
        status_code = request.session['status_code']
    except KeyError:
        message = None
        status_code = None
        
    request.session['message'] = None
    request.session['status_code'] = None

    # If they've signed up, save their data
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        course = Courselist.objects.get(name=request.POST["chosen_course"])

        # Save their new course 
        c = Course(user=user, course=course)
        c.save()

        # Try to get data from previous sign-ups for this course
        try:
            olds = OldProgress.objects.filter(user=user, course=course)
            
            # Find their old data
            for old in olds:
                progress = Progress(course=c, path=old.path, completed=old.completed)
                progress.save()
        except: 
            olds = None
        
        if not olds:
            # Otherwise, set setup all progress (with default=False)
            pathslist = []
            for p in Filepage.objects.filter(chapterpath=c.course.start.chapterpath):
                # and put them in a list as a tuple
                pathslist.append(p.path)
            
            for q in pathslist:
                path = Filepage.objects.get(chapterpath=c.course.start.chapterpath, path=q)
                progress = Progress(course=c, path=path)
                progress.save()

        # Redirect them to their user page
        return HttpResponseRedirect("/user")

    # If they want to see the page
    else:
        # Save their data
        user = User.objects.get(id=request.user.id)
       
        try:
            course = Course.objects.get(user=user)
        except:
            # Render their page, with the correct course
            courselist = Courselist.objects.all()

            return render(request, "home/user.html", {
                "course":None,
                "courselist":courselist,
                "message":message,
                "status_code":status_code
            })

        # A function that return an int of the path, so that it can be sorted
        def makeKey(progress):
            return int(progress.path.path)

        # Make a list of all progress (paragraphs) and sort it
        pathslist = Progress.objects.filter(course=course)
        pathslist = sorted(pathslist, key=makeKey)
        print(pathslist)

        # Render their page, with the correct course
        return render(request, "home/user.html", {
            "course":course,
            "pathslist":pathslist,
            "message":message,
            "status_code":status_code
        })

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
        request.session['message'] = "Je account is aangemaakt!"
        request.session['status_code'] = 1
        return HttpResponseRedirect(reverse("user"))
    
    else:
        # Render the template with the form
        return render(request, "home/register.html", {
            'form':form
        })

# Updates the progress of a user
def progress(request):
    if request.method == "POST":
        # Save their data
        uid = request.user.id
        user = User.objects.get(id=uid)
        path = request.POST["path"]

        # Get the course and the page they've completed
        course = Course.objects.get(user=user)
        page = Filepage.objects.get(chapterpath=course.course.start.chapterpath, path=path)

        # Update the progress
        p = Progress.objects.get(course=course, path=page)
        p.completed = True
        p.save()

        # Redirect them to their homepage
        return HttpResponseRedirect("/user")

# If they want to leave a course, this function runs
def leavecourse(request):
    # Save their data
    uid = request.user.id
    user = User.objects.get(id=uid)

    # Find their course
    course = Course.objects.get(user=user)
    
    # Find all their progress for this course
    progresses = Progress.objects.filter(course=course)
    for progress in progresses:
        # move it to the oldprogress table, if it already exists there, do nothing
        try:
            old = OldProgress.objects.get(user=progress.course.user, course=progress.course.course, path=progress.path)
            old.completed = progress.completed
        except OldProgress.DoesNotExist:
            old = OldProgress(user=progress.course.user, course=progress.course.course, path=progress.path, completed=progress.completed)
        old.save()
    # Delete the current course
    course.delete()
    # Redirect them to their homepage
    return HttpResponseRedirect("/user")

def about_us(request):
    return render(request, "home/about-us.html")

def pws(request):
    return render(request, "home/pws.html")

def contact(request):
    return render(request, "home/contact.html")
