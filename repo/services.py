import datetime
import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Tuple, Dict, Any, cast, Optional
from urllib.parse import urlparse

import requests
from django.core.validators import URLValidator
from git import Repo  # type: ignore
from github import Github

logger = logging.getLogger(__name__)

BITBUCKET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
RECENT_DATE = datetime.datetime.today() - datetime.timedelta(
    days=183
)  # About half a year
RECENT_DATE_STR = RECENT_DATE.strftime("%Y-%m-%d")

###
# Getting Metadata
###

validate_url = URLValidator()
hostname_to_source = {
    "github.com": "github",
    "bitbucket.org": "bitbucket",
}
source_to_base_url = {
    "bitbucket": "https://bitbucket.org",
    "github": "https://github.com",
}


@dataclass
class UrlMetadata:
    source: str
    owner: str
    repo: str


class UnsupportedURL(Exception):
    ...


def identify_source(repo_url: str) -> UrlMetadata:
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

    return UrlMetadata(source=source_name, owner=owner_name, repo=repo_name)


###
# Getting API Based Metadata
###


@dataclass
class ApiData:
    days_since_update: int
    days_since_create: int
    watchers: int
    pull_requests_open: int
    pull_requests_total: int
    has_issues: bool
    open_issues: int


def _calculate_date_deltas(repo_json: Dict[str, Any]) -> Tuple[int, int]:
    today = datetime.datetime.today()
    updated_on = repo_json.get("updated_on")
    created_on = repo_json.get("created_on")

    if updated_on:
        last_update = datetime.datetime.strptime(updated_on, BITBUCKET_DATETIME_FORMAT)
        update_delta = today.date() - last_update.date()
        days_since_update = update_delta.days
    else:
        days_since_update = -1

    if created_on:
        first_update = datetime.datetime.strptime(created_on, BITBUCKET_DATETIME_FORMAT)
        create_delta = today.date() - first_update.date()
        days_since_create = create_delta.days
    else:
        days_since_create = -1

    return days_since_create, days_since_update


def _get_pull_request_counts(repo_url: str) -> Tuple[int, int]:
    pulls_url = f"{repo_url}/pullrequests"

    params_open_only = [("state", "OPEN")]
    pulls_open = requests.get(pulls_url, params=params_open_only)
    pulls_open_json = pulls_open.json()

    params_all = [("state", "OPEN"), ("state", "MERGED"), ("state", "SUPERSEDED")]
    pulls_all = requests.get(pulls_url, params=params_all)
    pulls_all_json = pulls_all.json()

    return pulls_all_json.get("size", -1), pulls_open_json.get("size", -1)


def _get_watcher_count(repo_url: str) -> int:
    watchers_url = f"{repo_url}/watchers"
    watchers = requests.get(watchers_url)
    watchers_json = watchers.json()

    return cast(int, watchers_json.get("size", -1))


def _fetch_bitbucket_api_data(url_data: UrlMetadata) -> ApiData:
    # 1 Call Each:
    # Repo itself - 1
    # Watchers - 1
    # Pull Requests (open and total) - 2

    repo_url = (
        f"https://api.bitbucket.org/2.0/repositories/{url_data.owner}/{url_data.repo}"
    )
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


def _fetch_github_api_data(url_data: UrlMetadata) -> ApiData:
    # Calls:
    # Repo itself - 1
    # Pull Requests (open and total) - 2

    github_client = Github()
    repo = github_client.get_repo(f"{url_data.owner}/{url_data.repo}")
    logger.debug(repo)

    today = datetime.datetime.today()

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


def fetch_api_data(url_data: UrlMetadata) -> ApiData:
    """
    Make API calls required to get data from APIs
    """
    return fetch_source_map[url_data.source](url_data)


###
# Getting Git Repo Based Metadata
# Data:
#   - Commits (total, recent)
#   - Branches
#   - Authors
#   - Size of Codebase
###


@dataclass
class LocalData:
    commits_total: int
    commits_recent: int
    branch_count: int
    authors_total: int
    authors_recent: int
    lines_of_code_total: int
    files_total: int


def _setup_repo(directory_path: str, url_data: UrlMetadata) -> Repo:
    """
    Either clones or pulls the repo so that it has the latest data
    """

    if os.path.exists(directory_path):
        repo = Repo(directory_path)
        repo.remotes["origin"].pull()
    else:
        repo = Repo.clone_from(
            f"{source_to_base_url[url_data.source]}/{url_data.owner}/{url_data.repo}.git",
            to_path=directory_path,
            multi_options=["--filter=tree:0", "--single-branch"],
        )

    return repo


def _get_authors_commits(repo: Repo, recent: Optional[bool] = False) -> Tuple[int, int]:
    """
    Uses `git shortlog` to retrieve a list of authors and count the commits they've contributed
    """
    if recent:
        author_data = repo.git.shortlog(
            repo.active_branch, numbered=True, summary=True, since=RECENT_DATE_STR
        )
    else:
        author_data = repo.git.shortlog(repo.active_branch, numbered=True, summary=True)

    author_data_list = author_data.splitlines()
    authors_count = len(author_data_list)
    commit_count = 0

    for line in author_data_list:
        line = line.strip()
        count_str, _ = re.split(r"\s+", line, 1)
        commit_count += int(count_str)

    return authors_count, commit_count


class ClocMissingError(Exception):
    ...


def fetch_local_data(url_data: UrlMetadata) -> LocalData:
    """
    Calculates data about the git repo based on the local git files
    """
    directory_path = f"/tmp/gitgrade/{url_data.source}_{url_data.owner}_{url_data.repo}"
    repo = _setup_repo(directory_path, url_data)

    branch_list = repo.git.ls_remote(heads=True)
    branch_count = len(branch_list.splitlines())

    authors_count, commit_count = _get_authors_commits(repo)
    authors_count_recent, commit_count_recent = _get_authors_commits(repo, True)

    try:
        subprocess.run(["cloc", "--version"], check=True)
    except subprocess.CalledProcessError as error:
        raise ClocMissingError(
            "Please install cloc, it's required for understanding the size of the codebase."
        ) from error

    cloc = subprocess.run(
        ["cloc", "--quiet", "--json", directory_path], check=True, capture_output=True
    )
    cloc_stdout = cloc.stdout
    cloc_json = json.loads(cloc_stdout)

    return LocalData(
        commits_total=commit_count,
        commits_recent=commit_count_recent,
        branch_count=branch_count,
        authors_total=authors_count,
        authors_recent=authors_count_recent,
        lines_of_code_total=cloc_json.get("SUM", {}).get("code", -1),
        files_total=cloc_json.get("SUM", {}).get("nFiles", -1),
    )
