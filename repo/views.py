import logging
from dataclasses import asdict
from typing import Final
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .forms import RepoForm
from .models import GitRepoData
from .services.db_cache_service import check_cache, patch_cache
from .services.rest_api_service import fetch_api_data
from .services.local_git_service import fetch_local_data
from .services.url_service import identify_source

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
            url_metadata = identify_source(repo_url)

            try:
                api_data, local_data = check_cache(url_metadata)
            except GitRepoData.DoesNotExist:
                api_data = fetch_api_data(url_metadata)
                local_data = fetch_local_data(url_metadata)
                patch_cache(url_metadata, api_data, local_data)

            final_grade: Final = "Placeholder"
            response_json = {
                "url_metadata": asdict(url_metadata),
                "api_data": asdict(api_data),
                "local_data": asdict(local_data),
                "final_grade": final_grade,
            }
            return render(request, "repo/repo_results.html", response_json)
    else:
        form = RepoForm()

    return render(request, "repo/repo_input.html", {"form": form})
