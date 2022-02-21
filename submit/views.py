from urllib.error import HTTPError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.http.request import HttpHeaders, HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Input, Score, File, Key
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages

# Create your views here.

def index(request):
    scores = Score.objects.filter(user=request.user)
    results = {}
    for score in scores:
        score_list = [score.slug.rsplit("/", 1)[-1], score.passed_tests, score.total_tests]
        course = score.slug.rsplit("/", 1)[0]
        if course in results:
            results[course].append(score_list)
        else:
            results[course] = [score_list]

    return render(request,"submit/index.html", {
        'user':request.user,
        'results':results
    })


@csrf_exempt
def input(request):
    """ Receive input from a function that runs somewhere else and uploads that input (the result of an automated check to the database, so students can review their score on our webiste. """

    if request.method == "POST":

        # Save data
        import json
        result = request.POST['result']
        data = json.loads(result)
        slug = data['slug']

        # Check key
        if check_key(request.POST['key']):
            k = Key.objects.get(key=request.POST['key'])
            k.delete()
        else:
            raise Http404("De geheime sleutel is correct.") 

        # Get the user, based on the username given via POST
        u = User.objects.get(username=request.POST['username'])

        # Save this commit in the database
        i = Input(user=u, slug=slug, result=data, datetime=timezone.now())
        i.save()

        # Initialise for counting the amount of tests passed
        tests = data['results']
        passed = 0

        # Count of amount of tests passed
        for test in tests:
            if test['passed'] == True:
                passed += 1
        
        # Update the score object or create a new one, if this is the first time submitting to this slug
        try:
            s = Score.objects.get(user=u, slug=slug)
            s.total_tests = len(tests)
            s.passed_tests = passed
        except ObjectDoesNotExist:
            s = Score(user=u, slug=data['slug'], total_tests=len(tests), passed_tests=passed)
        s.save()

        # Store the files in the database
        files = request.POST['files']
        files = json.loads(files)

        for file_name in files:
            f = File(input=i, name=file_name, file=files[file_name])
            f.save()
        
        return HttpResponse("Gelukt!")

    return HttpResponse("Ik ben bang dat je verdwaald bent")

def check_username(request, username):
    """ Function that returns 200 if the username exists in the database and 404 is it does not. """

    try:
        u = User.objects.get(username=username)
    except:
        raise HTTPError("Gebruikersnaam niet gevonden.")
    
    return HttpResponse("Gevonden!")

def generate_key(request):
    """ Returns a key that can be sent along with the request to ensure a safe transaction. """

    def create_key():
        import string
        from random import choice
        characters = string.ascii_letters #+ string.punctuation  + string.digits
        password =  "".join(choice(characters) for x in range(25))
        return password
    
    key = create_key()

    response = HttpResponse('Verstuurd.')
    response.set_cookie('key', key)

    k = Key(key=key, when_requested=timezone.now())
    k.save()

    return response

def update_keylist():
    keys = Key.objects.all()
    
    now = timezone.now()
    
    for k in keys:
        difference = now - k.when_requested
        minutes = difference.total_seconds() / 60
        if minutes > 60:
            k.delete()

def check_key(key):

    update_keylist()

    keys = Key.objects.all()
    for k in keys:
        if str(k.key) == key:
            return True
    return False

def submission(request, username, problem):
    user = User.objects.get(username=username)
    
    inputs = []
    for input in Input.objects.filter(user=user, slug=problem).order_by('-datetime'):
        files = File.objects.filter(input=input)
        inputs.append((input, files))

    return render(request, "submit/submission.html", {
        'user':user,
        'problem':problem,
        'inputs':inputs
    })

def files(request, input_pk, filename):
    try:
        i = Input.objects.get(pk=input_pk)
    except:
        messages.add_message(request, messages.WARNING, 'Invalide link')
        return HttpResponseRedirect("/submit")

    if filename == "index":

        try:
            f = File.objects.filter(input=i)
            return render(request, "submit/file_index.html", {
                'user':request.user,
                'f':f
            })
        except:
            messages.add_message(request, messages.INFO, 'Geen bestanden gevonden.')
            return HttpResponseRedirect("/submit")
      
    try:
        f = File.objects.get(input=i, name=filename)
    except:
        messages.add_message(request, messages.WARNING, 'Dat bestand bestaat niet!')
        return HttpResponsePermanentRedirect("/submit")
     
    return render(request, "submit/file.html", {
        'user':request.user,
        'f':f
    })