from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repo-input/", views.repo_input, name="repo_input"),
]
