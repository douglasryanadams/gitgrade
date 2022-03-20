from dataclasses import dataclass, field
from typing import Optional

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24


@dataclass
class Statistics:
    mean: float
    standard_deviation: float
    majority: float = field(init=False)

    def __post_init__(self) -> None:
        self.majority = self.mean + self.standard_deviation


@dataclass
class RepoRequest:
    """
    This class represents the incoming request requirements
    for grading a repo
    """

    source: str
    owner: str
    repo: str
    sso_token: Optional[str] = None


@dataclass
class ViewOnly:
    commit_interval_days_all: str
    commit_interval_days_recent: str
