from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Filepage, LatestPage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# List of all the files in the database
def index(request):
    # Get the files from the database and render the template
    files = Filepage.objects.all()
    lptrue = False

    uid = request.user.id
    user = User.objects.get(id=uid)

    try:
        if user.latestpage:
            lptrue = True
    except:
        pass

    return render(request, 'files/index.html', {
        "files":files,
        "lptrue":lptrue
    })

# Basic view for viewing a file and updating the latestpage a user's visited
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
def latestpage(request):
    # Save the user's id
    uid = request.user.id
    user = User.objects.get(id=uid)

    # Try to find the user's latest page 
    try:
        latestpage = user.latestpage
        lpath = latestpage.path
        lchapterpath = latestpage.chapterpath
    # If that doesn't exist, redirect to the first page there is
    except:
        return HttpResponseRedirect("/files/h1/1")

    # Return a redirect to the correct path (/files/chapterpath/path)
    return HttpResponseRedirect("/files/" + lchapterpath + "/" + lpath)