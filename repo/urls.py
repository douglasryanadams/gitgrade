from django.urls import path

from . import views

urlpatterns = [
    path("", views.repo_input, name="landing"),
    path("result/", views.repo_grade, name="result_post"),
    path(
        "result/<str:source>/<str:owner>/<str:repo>",
        views.repo_grade,
        name="result_get",
    ),
]
