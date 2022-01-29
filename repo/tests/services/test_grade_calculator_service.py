# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest

from repo.services.data import LocalData, ApiData, Grade
from repo.services.grade_calculator_service import calculate_grade


@pytest.fixture
def base_api_data():
    """
    Baseline for raw data, represents "best case"
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
    Baseline for raw data, represents "best case"
    """
    return LocalData(
        days_since_commit=0,
        commits_total=52 * 3 * 10,  # Three per week for 10 years
        commits_recent=6 * 4 * 3,  # 3 per week for 6 months
        branch_count=-1,  # Doesn't matter
        authors_total=100,
        authors_recent=100,
        lines_of_code_total=10_000,
        files_total=5000,  # Average file 200 lines long
    )


def test_perfect_grade(base_api_data, base_local_data):
    assert calculate_grade(base_api_data, base_local_data) == Grade.A


def test_grade_a(base_api_data, base_local_data):
    base_local_data.days_since_commit = 15
    assert calculate_grade(base_api_data, base_local_data) == Grade.A


def test_grade_b(base_api_data, base_local_data):
    base_local_data.days_since_commit = 45
    assert calculate_grade(base_api_data, base_local_data) == Grade.B


def test_grade_c(base_api_data, base_local_data):
    base_local_data.days_since_commit = 75
    assert calculate_grade(base_api_data, base_local_data) == Grade.C


def test_grade_d(base_api_data, base_local_data):
    base_local_data.days_since_commit = 100
    assert calculate_grade(base_api_data, base_local_data) == Grade.D


def test_grade_f(base_api_data, base_local_data):
    base_local_data.days_since_commit = 400
    assert calculate_grade(base_api_data, base_local_data) == Grade.F
