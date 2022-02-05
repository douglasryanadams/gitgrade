from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class RepoRequestData:
    source: str
    owner: str
    repo: str
    sso_token: Optional[str] = None


@dataclass
class ApiData:
    days_since_update: int
    days_since_create: int
    watchers: int
    pull_requests_open: int
    pull_requests_total: int
    has_issues: bool
    open_issues: int


@dataclass
class LocalData:
    days_since_commit: int
    commits_total: int
    commits_recent: int
    branch_count: int
    authors_total: int
    authors_recent: int
    prolific_author_commits_total: int
    prolific_author_commits_recent: int
    lines_of_code_total: int
    files_total: int


class Grade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
