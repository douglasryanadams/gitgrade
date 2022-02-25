import json
import logging
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import stdev, median, fmean
from typing import Optional, List, Final

from git import Repo, Commit  # type: ignore

from repo.services.data import RepoRequestData, LocalData, Statistics
from repo.services.errors import ClocMissingError

logger = logging.getLogger(__name__)

source_to_base_url = {
    "bitbucket": "https://bitbucket.org",
    "github": "https://github.com",
}

RECENT_DAYS: Final = 183  # About half a year


def _setup_repo(directory_path: str, url_data: RepoRequestData) -> Repo:
    """
    Either clones or pulls the repo so that it has the latest data
    """

    if os.path.exists(directory_path):
        logger.debug("  repo already exists, pulling: %s", directory_path)
        repo = Repo(directory_path)
        repo.remotes["origin"].pull()
    else:
        repo_url = f"{source_to_base_url[url_data.source]}/{url_data.owner}/{url_data.repo}.git"
        logger.debug("  cloning repo from: %s", repo_url)
        logger.debug("  cloning repo to: %s", directory_path)

        repo = Repo.clone_from(
            repo_url,
            to_path=directory_path,
            multi_options=["--filter=tree:0", "--single-branch"],
        )

    return repo


@dataclass
class AuthorCommits:
    authors_count: int
    commit_count: int
    prolific_author_commits: int


def _get_authors_commits(repo: Repo, recent: Optional[bool] = False) -> AuthorCommits:
    """
    Uses `git shortlog` to retrieve a list of authors and count the commits they've contributed
    """
    logger.debug("  getting data about authors from: %s", repo)

    def _get_count_from_line(this_line: str) -> int:
        this_line = this_line.strip()
        parts = re.split(r"\s+", this_line, 1)
        count_str = parts[0]
        return int(count_str)

    recent_date = datetime.today() - timedelta(days=RECENT_DAYS)
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
        count_int = _get_count_from_line(line)
        commit_count += count_int

    logger.debug("  authors_count (recent=%s) : %s", recent, authors_count)
    logger.debug("  commit_count (recent=%s) : %s", recent, commit_count)

    prolific_author_commits = (
        _get_count_from_line(author_data_list[0]) if author_data_list else 0
    )

    return AuthorCommits(
        authors_count=authors_count,
        commit_count=commit_count,
        prolific_author_commits=prolific_author_commits,
    )


def _get_days_since_last_commit(repo: Repo) -> int:
    logger.info("  getting days since last commit from: %s", repo)
    last_commit: Commit = repo.head.commit
    last_commit_date = datetime.fromtimestamp(last_commit.committed_date)
    since_last_commit = datetime.today() - last_commit_date
    logger.debug("  days since last commit: %s", since_last_commit.days)
    return since_last_commit.days


def _get_commit_interval_stats(
    repo: Repo, recent: Optional[bool] = False
) -> Statistics:
    """
    Returns statistics on the interval between commits
    """
    recent_date = datetime.today() - timedelta(days=RECENT_DAYS)
    recent_seconds = (recent_date - datetime(1970, 1, 1)).total_seconds()

    deltas: List[int] = []
    previous_date = -1
    commit_iterator = repo.iter_commits()
    for commit in commit_iterator:
        if recent and commit.committed_date < recent_seconds:
            break

        if previous_date == -1:
            previous_date = commit.committed_date
            continue

        # We're going backwards from most recent -> first commit
        deltas.append(previous_date - commit.committed_date)
        previous_date = commit.committed_date

    if deltas:
        stats = Statistics(
            mean=fmean(deltas), median=median(deltas), standard_deviation=stdev(deltas)
        )
    else:
        stats = Statistics(mean=-1, median=-1, standard_deviation=-1)

    logger.debug("  stats: %s", stats)
    return stats


def fetch_local_data(url_data: RepoRequestData) -> LocalData:
    """
    Calculates data about the git repo based on the local git files
    """
    logger.info("Fetching data from local git checkout: %s", url_data)

    directory_path = f"/tmp/gitgrade/{url_data.source}_{url_data.owner}_{url_data.repo}"
    logger.debug("  git repo path: %s", directory_path)

    try:
        repo = _setup_repo(directory_path, url_data)

        branch_list = repo.git.ls_remote(heads=True)
        branch_count = len(branch_list.splitlines())
        logger.debug("  branch_count: %s", branch_count)

        total_author_commits = _get_authors_commits(repo)
        recent_author_commits = _get_authors_commits(repo, True)
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

        stats_all = _get_commit_interval_stats(repo)
        stats_recent = _get_commit_interval_stats(repo, recent=True)

        return LocalData(
            days_since_commit=days_since_commit,
            commits_total=total_author_commits.commit_count,
            commits_recent=recent_author_commits.commit_count,
            branch_count=branch_count,
            authors_total=total_author_commits.authors_count,
            authors_recent=recent_author_commits.authors_count,
            prolific_author_commits_total=total_author_commits.prolific_author_commits,
            prolific_author_commits_recent=recent_author_commits.prolific_author_commits,
            lines_of_code_total=cloc_json.get("SUM", {}).get("code", -1),
            files_total=cloc_json.get("SUM", {}).get("nFiles", -1),
            commit_interval_all_mean=stats_all.mean,
            commit_interval_all_stdev=stats_all.standard_deviation,
            commit_interval_recent_mean=stats_recent.mean,
            commit_interval_recent_stdev=stats_recent.standard_deviation,
        )
    finally:
        shutil.rmtree(directory_path)
