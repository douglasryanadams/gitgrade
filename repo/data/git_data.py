from dataclasses import dataclass

from repo.data.general import Statistics


@dataclass
class CodeData:
    lines_of_code: int
    file_count: int


@dataclass
class PullRequestData:
    count: int
    count_open: int


@dataclass
class CommitData:
    count: int
    count_primary_author: int
    interval: Statistics


@dataclass
class ContributorData:
    days_since_create: int
    days_since_commit: int
    # author_count_all: int
    author_count_recent: int


@dataclass
class PopularityData:
    watcher_count: int
    open_issue_count: int


@dataclass
class GitData:
    """
    This class represents data used in the service layer
    for grade calculations
    """

    # code: CodeData
    pull_request: PullRequestData
    # commit_all: CommitData
    commit_recent: CommitData
    contributor: ContributorData
    popularity: PopularityData
