import json
import logging
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Tuple, Optional

from git import Repo, Commit  # type: ignore

from repo.services.data import UrlMetadata, LocalData
from repo.services.errors import ClocMissingError

logger = logging.getLogger(__name__)

source_to_base_url = {
    "bitbucket": "https://bitbucket.org",
    "github": "https://github.com",
}


def _setup_repo(directory_path: str, url_data: UrlMetadata) -> Repo:
    """
    Either clones or pulls the repo so that it has the latest data
    """

    if os.path.exists(directory_path):
        logger.debug("  repo already exists, pulling: %s", directory_path)
        repo = Repo(directory_path)
        repo.remotes["origin"].pull()
    else:
        repo_url = f"{source_to_base_url[url_data.source]}/{url_data.owner}/{url_data.repo}.git"
        logger.debug("  cloing repo from: %s", repo_url)
        logger.debug("  cloning repo to: %s", directory_path)

        repo = Repo.clone_from(
            repo_url,
            to_path=directory_path,
            multi_options=["--filter=tree:0", "--single-branch"],
        )

    return repo


def _get_authors_commits(repo: Repo, recent: Optional[bool] = False) -> Tuple[int, int]:
    """
    Uses `git shortlog` to retrieve a list of authors and count the commits they've contributed
    """
    logger.debug("  getting data about authors from: %s", repo)
    recent_date = datetime.today() - timedelta(days=183)  # About half a year
    recent_date_str = recent_date.strftime("%Y-%m-%d")

    if recent:
        author_data = repo.git.shortlog(
            repo.active_branch, numbered=True, summary=True, since=recent_date_str
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

    logger.debug("  authors_count (recent=%s) : %s", recent, authors_count)
    logger.debug("  commit_count (recent=%s) : %s", recent, commit_count)
    return authors_count, commit_count


def _get_days_since_last_commit(repo: Repo) -> int:
    logger.info("  getting days since last commit from: %s", repo)
    last_commit: Commit = repo.head.commit
    last_commit_date = datetime.fromtimestamp(last_commit.committed_date)
    since_last_commit = datetime.today() - last_commit_date
    logger.debug("  days since last commit: %s", since_last_commit.days)
    return since_last_commit.days


def fetch_local_data(url_data: UrlMetadata) -> LocalData:
    """
    Calculates data about the git repo based on the local git files
    """
    logger.info("Fetching data from local git checkout: %s", url_data)

    directory_path = f"/tmp/gitgrade/{url_data.source}_{url_data.owner}_{url_data.repo}"
    logger.debug("  git repo path: %s", directory_path)

    repo = _setup_repo(directory_path, url_data)

    branch_list = repo.git.ls_remote(heads=True)
    branch_count = len(branch_list.splitlines())
    logger.debug("  branch_count: %s", branch_count)

    authors_count, commit_count = _get_authors_commits(repo)
    authors_count_recent, commit_count_recent = _get_authors_commits(repo, True)
    days_since_commit = _get_days_since_last_commit(repo)

    try:
        subprocess.run(["cloc", "--version"], check=True)
    except subprocess.CalledProcessError as error:
        raise ClocMissingError(
            "Please install cloc, it's required for understanding the size of the codebase."
        ) from error

    cloc_command = ["cloc", "--quiet", "--json", directory_path]
    logger.debug("  running command: %s", cloc_command)
    cloc = subprocess.run(cloc_command, check=True, capture_output=True)
    cloc_stdout = cloc.stdout
    logger.debug("  cloc_output: %s", cloc_stdout)
    cloc_json = json.loads(cloc_stdout)

    return LocalData(
        days_since_commit=days_since_commit,
        commits_total=commit_count,
        commits_recent=commit_count_recent,
        branch_count=branch_count,
        authors_total=authors_count,
        authors_recent=authors_count_recent,
        lines_of_code_total=cloc_json.get("SUM", {}).get("code", -1),
        files_total=cloc_json.get("SUM", {}).get("nFiles", -1),
    )
