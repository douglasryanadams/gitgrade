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
        commit_interval_all_mean=(60 * 60 * 24 * 5),  # 5 Days
        commit_interval_all_stdev=(60 * 60 * 24),  # 1 Day
        commit_interval_recent_mean=(60 * 60 * 5),
        commit_interval_recent_stdev=(60 * 60 * 24),
    )


def test_perfect_grade(base_api_data, base_local_data):
    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.A
    )


def test_grade_a(base_api_data, base_local_data):
    base_local_data.days_since_commit = 15
    base_api_data.days_since_create = 1200
    base_local_data.authors_total = 30
    base_local_data.authors_recent = 10
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.30)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.50)

    base_local_data.commit_interval_all_mean = 60 * 60 * 24 * 10
    base_local_data.commit_interval_all_stdev = 60 * 60 * 24
    base_local_data.commit_interval_recent_mean = 60 * 60 * 24 * 10
    base_local_data.commit_interval_recent_stdev = 60 * 60 * 24

    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.A
    )


def test_grade_b(base_api_data, base_local_data):
    base_local_data.days_since_commit = 45
    base_api_data.days_since_create = 800
    base_local_data.authors_total = 15
    base_local_data.authors_recent = 7
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.15)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.30)

    base_local_data.commit_interval_all_mean = 60 * 60 * 24 * 20
    base_local_data.commit_interval_all_stdev = 60 * 60 * 24 * 5
    base_local_data.commit_interval_recent_mean = 60 * 60 * 24 * 20
    base_local_data.commit_interval_recent_stdev = 60 * 60 * 24 * 5

    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.B
    )


def test_grade_c(base_api_data, base_local_data):
    base_local_data.days_since_commit = 75
    base_api_data.days_since_create = 400
    base_local_data.authors_total = 5
    base_local_data.authors_recent = 4
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.08)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.15)

    base_local_data.commit_interval_all_mean = 60 * 60 * 24 * 40
    base_local_data.commit_interval_all_stdev = 60 * 60 * 24 * 10
    base_local_data.commit_interval_recent_mean = 60 * 60 * 24 * 40
    base_local_data.commit_interval_recent_stdev = 60 * 60 * 24 * 10
    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.C
    )


def test_grade_d(base_api_data, base_local_data):
    base_local_data.days_since_commit = 100
    base_api_data.days_since_create = 200
    base_local_data.authors_total = 2
    base_local_data.authors_recent = 2
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.04)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.08)

    base_local_data.commit_interval_all_mean = 60 * 60 * 24 * 75
    base_local_data.commit_interval_all_stdev = 60 * 60 * 24 * 10
    base_local_data.commit_interval_recent_mean = 60 * 60 * 24 * 75
    base_local_data.commit_interval_recent_stdev = 60 * 60 * 24 * 10

    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.D
    )


def test_grade_f(base_api_data, base_local_data):
    base_local_data.days_since_commit = 400
    base_api_data.days_since_create = 100
    base_local_data.authors_total = 1
    base_local_data.authors_recent = 0
    base_local_data.prolific_author_commits_total = int(52 * 3 * 10 * 0.02)
    base_local_data.prolific_author_commits_recent = int(6 * 4 * 3 * 0.04)

    base_local_data.commit_interval_all_mean = 60 * 60 * 24 * 100
    base_local_data.commit_interval_all_stdev = 60 * 60 * 24 * 25
    base_local_data.commit_interval_recent_mean = 60 * 60 * 24 * 100
    base_local_data.commit_interval_recent_stdev = 60 * 60 * 24 * 25

    assert (
        calculate_grade(base_api_data, base_local_data).final_grade.letter_grade
        == Grade.F
    )
