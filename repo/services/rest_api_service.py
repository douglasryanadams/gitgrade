import logging
from datetime import datetime
from typing import Dict, Any, Tuple, cast

import requests
from github import Github

from repo.services.data import RepoRequestData, ApiData

logger = logging.getLogger(__name__)

BITBUCKET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


def _calculate_date_deltas(repo_json: Dict[str, Any]) -> Tuple[int, int]:
    logger.debug("  calculating date deltas")
    today = datetime.today()
    updated_on = repo_json.get("updated_on")
    created_on = repo_json.get("created_on")

    if updated_on:
        last_update = datetime.strptime(updated_on, BITBUCKET_DATETIME_FORMAT)
        update_delta = today.date() - last_update.date()
        days_since_update = update_delta.days
    else:
        days_since_update = -1

    if created_on:
        first_update = datetime.strptime(created_on, BITBUCKET_DATETIME_FORMAT)
        create_delta = today.date() - first_update.date()
        days_since_create = create_delta.days
    else:
        days_since_create = -1

    logger.debug("  days_since_create: %s", days_since_create)
    logger.debug("  days_since_update: %s", days_since_update)
    return days_since_create, days_since_update


def _get_pull_request_counts(repo_url: str) -> Tuple[int, int]:
    logger.debug("  calculating pull request count")
    pulls_url = f"{repo_url}/pullrequests"
    logger.debug("  making request to: %s", pulls_url)

    params_open_only = [("state", "OPEN")]
    pulls_open = requests.get(pulls_url, params=params_open_only)
    pulls_open_json = pulls_open.json()

    params_all = [("state", "OPEN"), ("state", "MERGED"), ("state", "SUPERSEDED")]
    pulls_all = requests.get(pulls_url, params=params_all)
    pulls_all_json = pulls_all.json()

    return pulls_all_json.get("size", -1), pulls_open_json.get("size", -1)


def _get_watcher_count(repo_url: str) -> int:
    logger.debug("  calculating watcher count")
    watchers_url = f"{repo_url}/watchers"
    logger.debug("  making request to: %s", watchers_url)
    watchers = requests.get(watchers_url)
    watchers_json = watchers.json()

    return cast(int, watchers_json.get("size", -1))


def _fetch_bitbucket_api_data(url_data: RepoRequestData) -> ApiData:
    # 1 Call Each:
    # Repo itself - 1
    # Watchers - 1
    # Pull Requests (open and total) - 2

    logger.debug("  fetching data from bitbucket for: %s", url_data)
    repo_url = (
        f"https://api.bitbucket.org/2.0/repositories/{url_data.owner}/{url_data.repo}"
    )
    logger.debug("  bitbucket repo_url: %s", repo_url)
    repo = requests.get(repo_url)
    repo_json = repo.json()

    days_since_create, days_since_update = _calculate_date_deltas(repo_json)

    watchers_count = _get_watcher_count(repo_url)

    pulls_all_count, pulls_open_count = _get_pull_request_counts(repo_url)

    return ApiData(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watchers=watchers_count,
        pull_requests_open=pulls_open_count,
        pull_requests_total=pulls_all_count,
        has_issues=repo_json.get("has_issues", False),
        open_issues=-1,
    )


def _fetch_github_api_data(repo_request_data: RepoRequestData) -> ApiData:
    # Calls:
    # Repo itself - 1
    # Pull Requests (open and total) - 2
    logger.debug("  fetching data from github for: %s", repo_request_data)
    github_client = Github(login_or_token=repo_request_data.sso_token)
    repo = github_client.get_repo(f"{repo_request_data.owner}/{repo_request_data.repo}")

    today = datetime.today()

    updated_delta = today.date() - repo.updated_at.date()
    days_since_update = updated_delta.days

    created_delta = today.date() - repo.created_at.date()
    days_since_create = created_delta.days

    open_pulls = repo.get_pulls(state="open")
    all_pulls = repo.get_pulls(state="all")

    return ApiData(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watchers=repo.watchers_count,
        pull_requests_open=open_pulls.totalCount,
        pull_requests_total=all_pulls.totalCount,
        has_issues=repo.has_issues,
        open_issues=repo.open_issues_count,
    )


fetch_source_map = {
    "bitbucket": _fetch_bitbucket_api_data,
    "github": _fetch_github_api_data,
}


def fetch_api_data(url_data: RepoRequestData) -> ApiData:
    """
    Make API calls required to get data from APIs
    """
    logger.info("Fetching data from APIs: %s", url_data)
    return fetch_source_map[url_data.source](url_data)
