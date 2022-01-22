import json
import logging
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Tuple, Optional

from git import Repo  # type: ignore

from repo.services.data import UrlMetadata, LocalData

logger = logging.getLogger(__name__)

RECENT_DATE = datetime.today() - timedelta(days=183)  # About half a year
RECENT_DATE_STR = RECENT_DATE.strftime("%Y-%m-%d")

source_to_base_url = {
    "bitbucket": "https://bitbucket.org",
    "github": "https://github.com",
}


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
