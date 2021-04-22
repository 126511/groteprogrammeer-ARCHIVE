from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.docsindex, name="docsindex"),
    path("<slug:term>/", views.definition, name="definition"),
    path("", views.page, name="page"),
    path("link/<slug:term>/", views.link, name="link")
]