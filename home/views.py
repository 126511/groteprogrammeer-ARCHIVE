from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Courselist, Progress, OldProgress, Teachers
from files.models import Filepage

# Create your views here.

def home_index(request):
    """ Decides whether to render index or user """

    # If the user's not logged in, go to /index, otherwise to /user
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/index")
    return HttpResponseRedirect("/user")


def login_view(request):
    """ Logs a user in, as long as they provide valid credentials """

    # Logs the user in via a form
    if request.method == "POST":

        # Cache the data provided and check the validity of the credentials
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If the user's credentials are valid
        if user is not None:

            # Log the user in
            login(request, user)

            # Redirect to 'next' attribute
            next = request.POST.get('next')
            if next:
                return HttpResponseRedirect(next)
            
            # If there is no next, redirect to user
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


def logout_view(request):
    """ Logs the user out """

    # Log the user out
    logout(request)

    # Render template with message
    return render(request, "home/index.html", {
        "message": "Je bent nu uitgelogd",
        "status_code":1
    })


def index(request):
    """ Render the template for the index page"""
    
    return render(request, "home/index.html")


@login_required
def user(request):
    """ Renders a user-specific template, as their dashboard """

    # Try to get the messages from session
    try:
        message = request.session['message']
        status_code = request.session['status_code']

    # If they are not their, make them None
    except KeyError:
        message = None
        status_code = None
        
    # Clear session
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
        pages = Filepage.objects.filter(chapterpath=course.start.chapterpath)

        # For each file page in this course,
        for page in pages:

            # Try to get the old progress and turn into new progress
            try:
                old = OldProgress.objects.get(user=user, filepage=page)
                progress = Progress(user=user, filepage=page, completed=old.completed)

            # Otherwise, make a new progress with compeleted false (as default)
            except:
                progress = Progress(user=user, filepage=page)

            # Save changes
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

        # Make a list of all progress (paragraphs) and sort it
        pages = Filepage.objects.filter(chapterpath=course.course.start.chapterpath)
        pages = sorted(pages, key=lambda page : int(page.path))

        # Prepare for storing lessons
        lessons = dict()

        # For each page, 
        for page in pages:

            # Try to get the completed status
            try:
                progress = Progress.objects.get(user=user, filepage=page).completed

            # If it does not exist (lesson is made after user signed up for course), set to false
            except:
                progress = False
            
            # Add to lessons
            lessons[page] = progress

        # Found out whether a user is a teacher
        teacher = False
        try:
            # Get their data from the teacher's model
            t = Teachers.objects.get(user=user)
            # If they are a teacher, set it to true
            if t.teacher:
                teacher = True
        # Else keep it false
        except:
            pass

        # Render their page, with the correct course and other data
        return render(request, "home/user.html", {
            "course":course,
            "lessons": lessons,
            "message":message,
            "status_code":status_code
        })


def register(request):
    """ Register a user """
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


def progress(request):
    """ Update the db that a user's finished a lesson"""

    if request.method == "POST":

        # Save their data
        user = User.objects.get(id=request.user.id)
        path = request.POST["path"]

        # Get the course and the page they've completed
        course = Course.objects.get(user=user)
        page = Filepage.objects.get(chapterpath=course.course.start.chapterpath, path=path)

        # Update the progress
        p = Progress.objects.get(user=user, filepage=page)
        p.completed = True
        p.save()

        # Redirect them to their homepage
        return HttpResponseRedirect("/user")


def leavecourse(request):
    """ Update the db that a user's left a course """

    # Save their data
    user = User.objects.get(id=request.user.id)

    # Find their course
    course = Course.objects.get(user=user)
    
    # Find all their progress for this course
    progresses = Progress.objects.filter(user=user)

    # For each lesson
    for progress in progresses:
        
        # Try to get the old progress and update it
        try:
            old = OldProgress.objects.get(user=user, filepage=progress.filepage)
            old.completed = progress.completed

        # If that does not exist, make a new one
        except OldProgress.DoesNotExist:
            old = OldProgress(user=user, filepage=progress.filepage, completed=progress.completed)

        # Save updates and delete progress for Progress table
        old.save()
        progress.delete()
    
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

# Homepage for all teachers
def teacher(request):
    # Get their user ids
    uid = request.user.id
    user = User.objects.get(id=uid)

    # Found out whether they are teachers
    try:
        # Get their data from teachers model
        t = Teachers.objects.get(user=user)
        # If their are not a teacher: redirect to correct page
        if t.teacher == False:
            return HttpResponseRedirect("/user")
    # If we didn't find them in the system, also redirect
    except:
        return HttpResponseRedirect("/user")

    # Render the correct page with corresponding data
    return render(request, "home/teacher.html")