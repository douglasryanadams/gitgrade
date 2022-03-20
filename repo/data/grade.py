from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class Grade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


@dataclass
class TestGrade:
    letter_grade: Grade
    points_max: float
    points_earned: float
    weight: float
    weight_str: str
    raw_number: Union[int, float]
    unit: Optional[str]


@dataclass
class TestGrades:
    days_since_commit: TestGrade
    days_since_create: TestGrade
    # author_count_all: TestGrade
    author_count_recent: TestGrade
    # commit_count_primary_author_all: TestGrade
    commit_count_primary_author_recent: TestGrade
    # commit_interval_all: TestGrade
    commit_interval_recent: TestGrade
    final_grade: TestGrade
