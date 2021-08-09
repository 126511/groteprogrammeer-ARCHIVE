from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Filepage, LatestPage
from docs.models import Term
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json
from home.models import Course, Courselist

# Create your views here.

# List of all the files in the database
@login_required
def index(request):
    # Set up a set with all chapterpaths and a dict with the all pages
    chapterpaths = set()
    pagedict = dict()

    # Populate the set of chapterpaths
    files = Filepage.objects.all()
    for file in files:
        chapterpaths.add(file.chapterpath)

    # For every chapterpath, find the corresponding paths and titles
    for chapterpath in sorted(chapterpaths):
        pathslist = list()
        for p in Filepage.objects.filter(chapterpath=chapterpath):
            # and put them in a list as a tuple
            curpage = (p.path, p.title)
            pathslist.append(curpage)
        # that is sorted, by the paths
        pathslist = sorted(pathslist, key=lambda tuplein : int(tuplein[0]))
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
    file = Filepage.objects.get(chapterpath=chapterpath, path=path)
    user = User.objects.get(id=request.user.id)
    
    # Save the latestpage, if possible
    try:
        user.latestpage.filepage = file
        user.latestpage.save()

    # The above raises an error if the user has no latestpage, then create one
    except ObjectDoesNotExist:
        page = LatestPage(user=user, filepage=file)
        page.save()

    # Get all documentation from the database and put in JSON format
    d = Term.objects.all()
    docs = dict()

    for every in d:
       docs[every.link] = every.definition
    
    jsonobj = json.dumps(docs) 

    # Render the template with the corresponding file
    return render(request, 'files/file_view.html', {
        'file':file,
        'docs':jsonobj,
    })

# Redirect a user to their latest page
@login_required
def latestpage(request):
    # Save the user's id
    user = User.objects.get(id=request.user.id)

    # Try to find the user's latest page 
    try:
        return HttpResponseRedirect("/files/" + user.latestpage.filepage.chapterpath + "/" + user.latestpage.filepage.path)
    # If it does not exist, redirect to the course's start
    except:
        course = Course.objects.get(user=user)
        return HttpResponseRedirect("/files/" + course.course.start.chapterpath + "/" + course.course.start.path)