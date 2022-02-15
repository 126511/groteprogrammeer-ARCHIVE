from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("input/", views.input, name="input"),
    path("check_username/<slug:username>", views.check_username, name="check_username"),
    path("generate_key/", views.generate_key, name="generate_key"),
    path("submission/<str:username>/<path:problem>", views.submission, name="submission"),
    path("files/<int:input_pk>/<str:filename>", views.files, name="files")
]