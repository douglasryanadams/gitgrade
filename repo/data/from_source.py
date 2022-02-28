from dataclasses import dataclass
from typing import Optional

from repo.data.general import Statistics


@dataclass
class TimeData:
    commits: int
    commits_primary_author: int
    commit_interval: Optional[Statistics]
    authors: int


@dataclass
class DataFromClone:
    days_since_commit: int
    branch_count: int
    lines_of_code_total: int
    files_total: int
    all: TimeData
    recent: TimeData