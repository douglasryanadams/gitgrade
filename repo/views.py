import logging
from typing import Optional

from django.conf import settings
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)

from .forms import RepoForm
from .services.input_service import input_util

logger = logging.getLogger(__name__)


def repo_input(request: HttpRequest) -> HttpResponse:
    """
    Returns a form for collecting the Repo URL we want to evaluate
    """
    logger.info("Received request %s", request)
    form = RepoForm()
    return render(request, "repo/repo_input.html", {"form": form})


def repo_grade(
    request: HttpRequest,
    source: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
) -> HttpResponse:
    github_token = request.COOKIES.get(settings.GITHUB_TOKEN_KEY)
    response_json = None
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]
            response_json = input_util(repo_url=repo_url, github_token=github_token)
    elif request.method == "GET":
        response_json = input_util(source=source, owner=owner, repo=repo, github_token=github_token)
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST", "GET"])

    if response_json:
        return render(request, "repo/repo_results.html", response_json)

    return HttpResponseServerError()
