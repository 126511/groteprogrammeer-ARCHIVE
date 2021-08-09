from django.shortcuts import render
from .models import Term
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def docsindex(request):
    docs = set()

    terms = Term.objects.all()

    for t in terms:
        docs.add(t)

    docs = sorted(docs, key=lambda doc: doc.term)

    return render(request, "docs/index.html", {
        "docs":docs
    })

def definition(request, term):
    
    t = Term.objects.get(link=term)

    return render(request, "docs/definition.html", {
        "term":t
    })

def page(request):
    return render(request, "docs/page.html")

def link(request, term):
    return render(request, "docs/page.html", {
        "redirect":term
    })