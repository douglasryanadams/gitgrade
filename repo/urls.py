from django.urls import path

from . import views

urlpatterns = [
    path("", views.repo_input, name="landing"),
]
