from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, LatestVisit
from docs.models import Term
from django.core.exceptions import ObjectDoesNotExist
import json
from home.models import UserToChapter
from django.contrib import messages

# Create your views here.

# List of all the files in the database
@login_required
def index(request):
    # Set up a set with all chapterpaths and a dict with the all pages
    chapterpaths = set()
    pagedict = dict()

    # Populate the set of chapterpaths
    lessons = Lesson.objects.all()
    for lesson in lessons:
        chapterpaths.add(lesson.chapterpath)

    # For every chapterpath, find the corresponding paths and titles
    for chapterpath in sorted(chapterpaths):
        pathslist = list()
        for lesson in Lesson.objects.filter(chapterpath=chapterpath).order_by('path'):
            # and put them in a list as a tuple
            current_lesson = (lesson.path, lesson.title)
            pathslist.append(current_lesson)
        # and then connect the chapterpath to that list in pagedict
        pagedict[chapterpath] = pathslist

    # Return the index with a list of the files and whether the user has a last page
    return render(request, 'files/index.html', {
        "pagedict":pagedict,
    })

# Basic view for viewing a file and updating the latestpage a user's visited
@login_required
def file_view(request, chapterpath, path):
    # Query for the file and save the user's id
    try:
        lesson = Lesson.objects.get(chapterpath=chapterpath, path=path)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, 'Die les bestaat niet!')
        return HttpResponseRedirect("/")
    
    user = request.user
    
    # Save the latestpage, if possible
    try:
        user.latestvisit.lesson = lesson
        user.latestvisit.save()

    # The above raises an error if the user has no latestpage, then create one
    except ObjectDoesNotExist:
        page = LatestVisit(user=user, lesson=lesson)
        page.save()

    # Get all documentation from the database and put in JSON format
    d = Term.objects.all()
    docs = dict()

    for every in d:
       docs[every.link] = every.definition
    
    jsonobj = json.dumps(docs) 

    user2chapter = UserToChapter.objects.get(user=user)
    coursefiles = Lesson.objects.filter(chapterpath=user2chapter.chapter.path)

    file_in_course = False
    if lesson in coursefiles:
        file_in_course = True
    
    print(file_in_course)

    # Render the template with the corresponding file
    return render(request, 'files/file_view.html', {
        'file':lesson,
        'docs':jsonobj,
        'file_in_course':file_in_course
    })

# Redirect a user to their latest page
@login_required
def latestpage(request):
    # Save the user's id
    user = request.user

    # Try to find the user's latest page 
    try:
        lesson = user.latestvisit.lesson
        return HttpResponseRedirect("/files/" + lesson.chapterpath + "/" + lesson.path)
    # If it does not exist, redirect to the course's start
    except:
        chapter = UserToChapter.objects.get(user=user).chapter
        lesson = Lesson.objects.filter(chapterpath=chapter.path).order_by('path')[0]
        return HttpResponseRedirect("/files/" + lesson.chapterpath + "/" + lesson.path)