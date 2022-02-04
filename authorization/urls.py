from django.urls import path

from . import views

urlpatterns = [
    path("github", views.github_authorization, name="github"),
]
