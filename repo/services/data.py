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
    commit_interval_all_mean: float
    commit_interval_all_stdev: float
    commit_interval_recent_mean: float
    commit_interval_recent_stdev: float


@dataclass
class Statistics:
    mean: float
    median: float
    standard_deviation: float


class Grade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


@dataclass
class TestGrade:
    letter_grade: Grade
    weight: float


@dataclass
class TestGrades:
    days_since_commit: TestGrade
    repo_age: TestGrade
    total_authors: TestGrade
    recent_authors: TestGrade
    total_prolific_authors: TestGrade
    recent_prolific_authors: TestGrade
    all_commit_interval: TestGrade
    recent_commit_interval: TestGrade
    final_grade: TestGrade
