# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest

from repo.services.data import LocalData, ApiData, Grade
from repo.services.grade_calculator_service import calculate_grade


@pytest.fixture
def base_api_data():
    """
    Baseline for raw data, represents "perfect case"
    """
    return ApiData(
        days_since_update=0,
        days_since_create=365 * 10,  # 10 years
        watchers=100,
        pull_requests_open=0,
        pull_requests_total=52 * 10,  # One per week for 10 years
        has_issues=True,
        open_issues=0,
    )


@pytest.fixture
def base_local_data():
    """
    Baseline for raw data, represents "perfect case"
    """
    return LocalData(
        days_since_commit=0,
        commits_total=52 * 3 * 10,  # Three per week for 10 years
        commits_recent=6 * 4 * 3,  # 3 per week for 6 months
        branch_count=-1,  # Doesn't matter
        authors_total=100,
        authors_recent=100,
        prolific_author_commits_total=52 * 3 * 10,
        prolific_author_commits_recent=6 * 4 * 3,
        lines_of_code_total=10_000,
        files_total=5000,  # Average file 200 lines long
    )


def test_perfect_grade(base_api_data, base_local_data):
    assert calculate_grade(base_api_data, base_local_data) == Grade.A


def test_grade_a(base_api_data, base_local_data):
    base_local_data.days_since_commit = 15
    base_api_data.days_since_create = 1200
    base_local_data.authors_total = 30
    base_local_data.authors_recent = 10
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.80)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.80)
    assert calculate_grade(base_api_data, base_local_data) == Grade.A


def test_grade_b(base_api_data, base_local_data):
    base_local_data.days_since_commit = 45
    base_api_data.days_since_create = 800
    base_local_data.authors_total = 15
    base_local_data.authors_recent = 7
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.75)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.75)
    assert calculate_grade(base_api_data, base_local_data) == Grade.B


def test_grade_c(base_api_data, base_local_data):
    base_local_data.days_since_commit = 75
    base_api_data.days_since_create = 400
    base_local_data.authors_total = 5
    base_local_data.authors_recent = 4
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.55)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.55)
    assert calculate_grade(base_api_data, base_local_data) == Grade.C


def test_grade_d(base_api_data, base_local_data):
    base_local_data.days_since_commit = 100
    base_api_data.days_since_create = 200
    base_local_data.authors_total = 2
    base_local_data.authors_recent = 2
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.45)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.45)
    assert calculate_grade(base_api_data, base_local_data) == Grade.D


def test_grade_f(base_api_data, base_local_data):
    base_local_data.days_since_commit = 400
    base_api_data.days_since_create = 100
    base_local_data.authors_total = 1
    base_local_data.authors_recent = 0
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.25)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.25)
    assert calculate_grade(base_api_data, base_local_data) == Grade.F


# pylint: disable=fixme
# TODO: Add some checks based on real repos as a "gut check" that we're in the ball-park
#       as we calibrate the grading system.
