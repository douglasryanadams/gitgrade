import logging
from datetime import datetime, timedelta
from typing import List, Dict

from github import Github
from github.Commit import Commit
from github.PaginatedList import PaginatedList

from repo.data.from_source import DataFromAPI, TimeData
from repo.data.general import RepoRequest, Statistics
from repo.services.util import get_statistics

logger = logging.getLogger(__name__)

BITBUCKET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


def _get_commit_data(
    commits: PaginatedList,  # type: ignore  # mypy wants PaginatedList[Commit] but pylint and python don't like it
) -> TimeData:
    logger.info("Getting commit data from APIs")
    deltas: List[float] = []
    previous_date = None
    commit_count = 0
    commits_by_author: Dict[str, int] = {}
    popular_author_count = 0

    for commit in commits:
        commit_count += 1
        commit_author = commit.commit.author
        logger.debug("  author: %s", commit_author.name)
        commits_this_author = commits_by_author.get(commit_author.name, 0) + 1
        commits_by_author[commit_author.name] = commits_this_author
        logger.debug("  commits so far: %s", commits_this_author)

        if commits_this_author > popular_author_count:
            popular_author_count = commits_this_author

        commit_date = commit_author.date
        logger.debug("  commit date: %s", commit_date)
        if previous_date is None:
            previous_date = commit_date
            continue

        deltas.append((previous_date - commit_date).total_seconds())
        previous_date = commit_date

    if deltas:
        commit_stats = get_statistics(deltas)
    else:
        commit_stats = Statistics(mean=0, standard_deviation=0)

    return TimeData(
        commit_count=commit_count,
        commit_count_primary_author=popular_author_count,
        commit_interval=commit_stats,
        author_count=len(commits_by_author),
    )


def _get_days_since_last_commit(commit: Commit) -> int:
    logger.info("  getting days since last commit")
    latest_commit = commit.commit.author.date
    since_last_commit = datetime.today() - latest_commit
    return since_last_commit.days


def fetch_github_api_data(repo_request_data: RepoRequest) -> DataFromAPI:
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

    six_months_ago = datetime.today() - timedelta(days=182)
    recent_commits = repo.get_commits(since=six_months_ago)
    time_data_recent = _get_commit_data(recent_commits)

    days_since_last_commit = _get_days_since_last_commit(recent_commits[0])

    branch_count = repo.get_branches().totalCount

    return DataFromAPI(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watcher_count=repo.watchers_count,
        pull_request_count_open=open_pulls.totalCount,
        pull_request_count=all_pulls.totalCount,
        has_issues=repo.has_issues,
        open_issue_count=repo.open_issues_count,
        days_since_commit=days_since_last_commit,
        branch_count=branch_count,
        time_recent=time_data_recent,
    )
