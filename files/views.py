from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Filepage, LatestPage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# List of all the files in the database
@login_required
def index(request):
    # Set up a set with all chapterpaths and a dict with the paths
    chapterpaths = set()
    pathsdict = dict()

    # Populate the set of chapterpaths
    files = Filepage.objects.all()
    for file in files:
        chapterpaths.add(file.chapterpath)

    # For every chapterpath, find the corresponding paths
    for chapterpath in chapterpaths:
        paths = []
        for p in Filepage.objects.filter(chapterpath=chapterpath):
            # and put them in a list,
            paths.append(p.path)
        # and then connect the chapterpath to that list in pathsdict
        pathsdict[chapterpath] = paths

    # Set up the lastpagetrue variable
    lptrue = False

    # Save user's id
    uid = request.user.id
    user = User.objects.get(id=uid)

    # Check whether the user has a latest page
    try:
        if user.latestpage:
            lptrue = True
    except:
        pass

    # Return the index with a list of the files and whether the user has a last page
    return render(request, 'files/index.html', {
        "lptrue":lptrue,
        "pathsdict":pathsdict
    })

# Basic view for viewing a file and updating the latestpage a user's visited
@login_required
def file_view(request, chapterpath, path):
    # Query for the file and save the user's id
    file = Filepage.objects.get(chapterpath=chapterpath, path=path)
    uid = request.user.id
    user = User.objects.get(id=uid)
    
    # Save the latestpage, if possible
    try:
        latestpage = user.latestpage
        latestpage.path = path
        latestpage.chapterpath = chapterpath
        latestpage.save()

    # The above raises an error if the user has no latestpage, then create one
    except ObjectDoesNotExist:
        page = LatestPage(user=user, path=path, chapterpath=chapterpath)
        page.save()

    # Render the template with the corresponding file
    return render(request, 'files/file_view.html', {
        'file':file,
    })

# Redirect a user to their latest page
@login_required
def latestpage(request):
    # Save the user's id
    uid = request.user.id
    user = User.objects.get(id=uid)

    # Try to find the user's latest page 
    latestpage = user.latestpage
    lpath = latestpage.path
    lchapterpath = latestpage.chapterpath


    # Return a redirect to the correct path (/files/chapterpath/path)
    return HttpResponseRedirect("/files/" + lchapterpath + "/" + lpath)