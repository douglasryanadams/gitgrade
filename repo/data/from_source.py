from dataclasses import dataclass
from typing import Optional

from repo.data.general import Statistics


@dataclass
class AuthorCommits:
    author_count: int
    commit_count: int
    commit_count_primary_author: int


@dataclass
class TimeData:
    commit_count: int
    commit_count_primary_author: int
    commit_interval: Statistics
    author_count: int


@dataclass
class DataFromClone:
    days_since_commit: int
    branch_count: int
    lines_of_code: int
    file_count: int
    time_all: TimeData
    time_recent: TimeData


@dataclass
class DataFromAPI:
    days_since_update: int
    days_since_create: int
    watcher_count: int
    pull_request_count_open: int
    pull_request_count: int
    open_issue_count: int

    days_since_commit: int
    time_recent: TimeData

    latest_release: str
    releases_count: int
    days_since_last_release: Optional[int]
