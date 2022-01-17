import datetime
import logging
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import requests
from django.core.validators import URLValidator
from github import Github

from gitgrade import Constants

logger = logging.getLogger(__name__)

###
# Getting Metadata
###

validate_url = URLValidator()
hostname_to_source = {
    "github.com": "github",
    "bitbucket.org": "bitbucket",
}


@dataclass
class SourceMetadata:
    source: str
    owner: str
    repo: str


class UnsupportedURL(Exception):
    ...


def identify_source(repo_url: str) -> SourceMetadata:
    """
    This method returns metadata about the repo based on the URL

    :param repo_url: URL of the repo we want to grade
    :return SourceMetadata: Object containing metadata we can extract from the URL
    """
    logger.info("Identifying source of: %s", repo_url)
    validate_url(repo_url)

    parsed_url = urlparse(repo_url)
    hostname = parsed_url.hostname
    if hostname:
        source_name = hostname_to_source.get(hostname)
    else:
        raise UnsupportedURL(f"{repo_url} does not contain a valid hostname")

    if not source_name:
        raise UnsupportedURL(f"{repo_url} is not currently supported")

    path = parsed_url.path
    path_parts = path.split("/")

    # If we add support for something that doesn't match this pattern, we should refactor
    owner_name = path_parts[1]
    repo_name = path_parts[2]

    return SourceMetadata(source=source_name, owner=owner_name, repo=repo_name)


###
# Getting API Based Metadata
###

@dataclass
class ApiBasedData:
    days_since_update: int
    days_since_create: int
    watchers: int
    pull_requests_open: int
    pull_requests_total: int
    has_issues: bool
    open_issues: int


def _calculate_date_deltas(repo_json):
    today = datetime.datetime.today()
    updated_on = repo_json.get("updated_on")
    created_on = repo_json.get("created_on")
    if updated_on:
        last_update = datetime.datetime.strptime(
            updated_on, Constants.BITBUCKET_DATETIME_FORMAT
        )
        update_delta = today.date() - last_update.date()
        days_since_update = update_delta.days
    else:
        days_since_update = -1
    if created_on:
        first_update = datetime.datetime.strptime(
            created_on, Constants.BITBUCKET_DATETIME_FORMAT
        )
        create_delta = today.date() - first_update.date()
        days_since_create = create_delta.days
    else:
        days_since_create = -1
    return days_since_create, days_since_update


def get_pull_request_counts(repo_url):
    pulls_url = f"{repo_url}/pullrequests"

    params_open_only = [("state", "OPEN")]
    pulls_open = requests.get(pulls_url, params=params_open_only)
    pulls_open_json = pulls_open.json()

    params_all = [("state", "OPEN"), ("state", "MERGED"), ("state", "SUPERSEDED")]
    pulls_all = requests.get(pulls_url, params=params_all)
    pulls_all_json = pulls_all.json()

    return pulls_all_json.get('size', -1), pulls_open_json.get('size', -1)


def _get_watcher_count(repo_url):
    watchers_url = f"{repo_url}/watchers"
    watchers = requests.get(watchers_url)
    watchers_json = watchers.json()
    return watchers_json.get('size', -1)


def _fetch_bitbucket(source: SourceMetadata) -> ApiBasedData:
    # 1 Call Each:
    # Repo itself - 1
    # Watchers - 1
    # Pull Requests (open and total) - 2

    repo_url = (
        f"{Constants.BITBUCKET_API_URL}/repositories/{source.owner}/{source.repo}"
    )
    repo = requests.get(repo_url)
    repo_json = repo.json()

    days_since_create, days_since_update = _calculate_date_deltas(repo_json)

    watchers_count = _get_watcher_count(repo_url)

    pulls_all_count, pulls_open_count = get_pull_request_counts(repo_url)

    return ApiBasedData(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watchers=watchers_count,
        pull_requests_open=pulls_open_count,
        pull_requests_total=pulls_all_count,
        has_issues=repo_json.get("has_issues", False),
        open_issues=-1,
    )


def _fetch_github(source: SourceMetadata) -> ApiBasedData:
    # Calls:
    # Repo itself - 1
    # Pull Requests (open and total) - 2

    github_client = Github()
    repo = github_client.get_repo(f'{source.owner}/{source.repo}')
    logger.debug(repo)

    today = datetime.datetime.today()

    updated_delta = today.date() - repo.updated_at.date()
    days_since_update = updated_delta.days

    created_delta = today.date() - repo.created_at.date()
    days_since_create = created_delta.days

    open_pulls = repo.get_pulls(state='open')
    all_pulls = repo.get_pulls(state='all')

    return ApiBasedData(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watchers=repo.watchers_count,
        pull_requests_open=open_pulls.totalCount,
        pull_requests_total=all_pulls.totalCount,
        has_issues=repo.has_issues,
        open_issues=repo.open_issues_count,
    )


fetch_source_map = {"bitbucket": _fetch_bitbucket, "github": _fetch_github}


def fetch_api_based_data(source: SourceMetadata) -> ApiBasedData:
    """
    Make API calls required to get data from APIs
    """
    return fetch_source_map[source.source](source)


def _extract_page_count(link_header_value: str) -> int:
    """
    Extract the page count, lets us count the resources (like contributors) without pulling them all
    """
    matches = re.search(r'[^&]&page=(\d+)>; rel="last"', link_header_value)

    if matches:
        page_count_str = matches.group(1)
        return int(page_count_str)

    return 0

###
# Getting Git Repo Based Metadata
# Data:
#   - Commits (total, recent)
#   - Branches
#   - Authors
#   - Size of Codebase
###
