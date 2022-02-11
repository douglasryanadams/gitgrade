import logging

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .forms import RepoForm
from .services.repo_input_service import repo_input_util

logger = logging.getLogger(__name__)


def repo_input(request: HttpRequest) -> HttpResponse:
    """
    Returns a form for collecting the Repo URL we want to evaluate
    """
    logger.info("Received request %s", request)
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]
            github_token = request.COOKIES.get(settings.GITHUB_TOKEN_KEY)

            response_json = repo_input_util(repo_url, github_token)

            return render(request, "repo/repo_results.html", response_json)
    else:
        form = RepoForm()

    return render(request, "repo/repo_input.html", {"form": form})
