from dataclasses import dataclass


@dataclass
class UrlMetadata:
    source: str
    owner: str
    repo: str


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
    commits_total: int
    commits_recent: int
    branch_count: int
    authors_total: int
    authors_recent: int
    lines_of_code_total: int
    files_total: int
