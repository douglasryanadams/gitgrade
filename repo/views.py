import logging
from dataclasses import asdict
from typing import Final

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .forms import RepoForm
from .services.data import Grade
from .services.db_cache_service import check_cache, patch_cache
from .services.errors import CacheMiss
from .services.grade_calculator_service import calculate_grade
from .services.rest_api_service import fetch_api_data
from .services.local_git_service import fetch_local_data
from .services.url_service import identify_source

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
            repo_data = identify_source(repo_url)

            try:
                api_data, local_data = check_cache(repo_data)
            except CacheMiss:
                github_token = request.COOKIES.get(settings.GITHUB_TOKEN_KEY)
                repo_data.sso_token = github_token

                api_data = fetch_api_data(repo_data)
                local_data = fetch_local_data(repo_data)
                patch_cache(repo_data, api_data, local_data)

            final_grade: Final[Grade] = calculate_grade(api_data, local_data)
            response_json = {
                "final_grade": final_grade.value,
                "metadata": asdict(repo_data),
                **asdict(api_data),
                **asdict(local_data),
            }
            return render(request, "repo/repo_results.html", response_json)
    else:
        form = RepoForm()

    return render(request, "repo/repo_input.html", {"form": form})
