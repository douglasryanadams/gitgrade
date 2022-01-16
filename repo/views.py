import logging
from typing import Final
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .forms import RepoForm

from .services import identify_source

logger = logging.getLogger(__name__)


def index(_: HttpRequest) -> HttpResponse:
    """
    Placeholder page for this path
    """
    return HttpResponse("Hello, world")


def repo_input(request: HttpRequest) -> HttpResponse:
    """
    Returns a form for collecting the Repo URL we want to evaluate
    """
    logger.info("Received request %s", request)
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]
            source = identify_source(repo_url)

            final_grade: Final = "Placeholder"
            response_json = {"source": source, "final_grade": final_grade}
            return HttpResponse(f"{response_json}")
    else:
        form = RepoForm()

    return render(request, "repo/repo_input.html", {"form": form})
