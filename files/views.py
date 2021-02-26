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
    # Get the files from the database and setup-up the lastpagetrue variable
    files = Filepage.objects.all()
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
    latestpage = user.latestpage
    lpath = latestpage.path
    lchapterpath = latestpage.chapterpath


    # Return a redirect to the correct path (/files/chapterpath/path)
    return HttpResponseRedirect("/files/" + lchapterpath + "/" + lpath)