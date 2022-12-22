from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.forms import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter, UserToChapter, Progress, OldProgress, Teacher
from files.models import Lesson
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home_index(request):
    """ Decides whether to render index or user """

    # If the user's logged in, go to /user, otherwise to /index
    if request.user.is_authenticated:
        return HttpResponseRedirect("/user")
    return HttpResponseRedirect("/index")


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
            messages.add_message(request, messages.SUCCESS, 'Je bent ingelogd!')

            # Redirect to 'next' attribute
            next = request.POST.get('next')
            if next:
                return HttpResponseRedirect(next)
            
            # If there is no next, redirect to user
            return HttpResponseRedirect("/user")

        # If the user's credentials are not valid
        else:
            # Let them try again and shout at them
            messages.add_message(request, messages.ERROR, 'Je gebruikersnaam en wachtwoord komen niet overeen!')
            return HttpResponseRedirect('/login')

    # Render the form for the user so they can log in
    else:
        return render(request, "home/login.html")


def logout_view(request):
    """ Logs the user out """

    # Log the user out
    logout(request)

    # Render template with message
    messages.add_message(request, messages.SUCCESS, 'Je bent nu uitgelogd.')
    return HttpResponseRedirect("/index")


def index(request):
    """ Render the template for the index page"""
    
    return render(request, "home/index.html")


@login_required
def user(request):
    """ Renders a user-specific template, as their dashboard """

    # If they've signed up, save their data
    if request.method == "POST":
        user = request.user
        chapterpath = request.POST['chosen_chapter']
        chapter = Chapter.objects.get(path=chapterpath)

        # Save their new course 
        c = UserToChapter(user=user, chapter=chapter)
        c.save()

        # Try to get data from previous sign-ups for this course
        lessons = Lesson.objects.filter(chapterpath=chapterpath)

        # For each file page in this course,
        for lesson in lessons:

            # Try to get the old progress and turn into new progress
            try:
                old = OldProgress.objects.get(user=user, lesson=lesson)
                progress = Progress(user=user, lesson=lesson, completed=old.completed)

            # Otherwise, make a new progress with compeleted false (as default)
            except ObjectDoesNotExist:
                progress = Progress(user=user, lesson=lesson)

            # Save changes
            progress.save()

        # Redirect them to their user page
        messages.add_message(request, messages.SUCCESS, f'We hebben je ingeschreven voor je nieuwe hoofdstuk!')
        return HttpResponseRedirect("/user")

    # If they want to see the page
    else:
        # Save their data
        user = request.user
       
        try:
            chapter = UserToChapter.objects.get(user=user).chapter
        except ObjectDoesNotExist:
            # Render their page, with the correct course
            chapters = Chapter.objects.all()

            return render(request, "home/user.html", {
                "chapters":chapters,
            })

        # Make a list of all progress (lessons) and sort it
        lessons = Lesson.objects.filter(chapterpath=chapter.path).order_by('path')

        # Prepare for storing lessons
        progresses = dict()

        # For each page, 
        for lesson in lessons:

            # Try to get the completed status
            try:
                progress = Progress.objects.get(user=user, lesson=lesson).completed

            # If it does not exist (lesson is made after user signed up for course), set to false
            except ObjectDoesNotExist:
                progress = False
            
            # Add to lessons
            progresses[lesson] = progress

        # Render their page, with the correct course and other data
        return render(request, "home/user.html", {
            "chapter":chapter,
            "progresses": progresses,
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
        messages.add_message(request, messages.SUCCESS, 'Welkom op GroteProgrammeer.nl!')
        return HttpResponseRedirect(reverse("user"))
    
    else:
        # Render the template with the form
        return render(request, "home/register.html", {
            'form':form
        })


def progress(request):
    """ Update the db that a user's finished a lesson """

    if request.method == "POST":

        # Save their data
        user = request.user
        path = request.POST["path"]

        # Get the course and the page they've completed
        chapter = UserToChapter.objects.get(user=user).chapter
        lesson = Lesson.objects.get(chapterpath=chapter.path, path=path)

        # Update the progress
        try:
            p = Progress.objects.get(user=user, lesson=lesson)
            p.completed = True
        except ObjectDoesNotExist:
            p = Progress(user=user, lesson=lesson, completed=True)
        
        p.save()

        # Redirect them to their homepage
        messages.add_message(request, messages.INFO, f'Je hebt {lesson.title} afgemaakt!')
        return HttpResponseRedirect("/user")
    
    return HttpResponse('Ik ben bang dat je verdwaald bent...')


def leavecourse(request):
    """ Update the db that a user's left a course """

    # Save their data
    user = request.user

    # Find their course
    try:
        user2chapter = UserToChapter.objects.get(user=user)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, 'Je bent niet ingeschreven voor een hoofdstuk en kan je dus ook niet uitschrijven.')
        return HttpResponseRedirect("/user")
    
    # Find all their progress for this course
    progresses = Progress.objects.filter(user=user)

    # For each lesson
    for progress in progresses:
        
        # Try to get the old progress and update it
        try:
            old = OldProgress.objects.get(user=user, lesson=progress.lesson)
            old.completed = progress.completed

        # If that does not exist, make a new one
        except ObjectDoesNotExist:
            old = OldProgress(user=user, lesson=progress.lesson, completed=progress.completed)

        # Save updates and delete progress for Progress table
        old.save()
        progress.delete()
    
    # Delete the current course
    user2chapter.delete()
    
    # Redirect them to their homepage
    messages.add_message(request, messages.SUCCESS, f'We hebben je uitgeschreven voor {user2chapter.chapter.name}')
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
    user = request.user

    # Found out whether they are teachers
    try:
        # Get their data from teachers model
        t = Teacher.objects.get(user=user)
        # If their are not a teacher: redirect to correct page
        if t.teacher == True:
                # Render the correct page with corresponding data
                return render(request, "home/teacher.html")
    # If we didn't find them in the system, also redirect
    except ObjectDoesNotExist:
        pass
    
    messages.add_message(request, messages.WARNING, 'Jij bent geen leraar en kan dus niet in het lerarenportaal!')
    return HttpResponseRedirect("/user")

