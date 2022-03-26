# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest

from repo.data.general import Statistics, SECONDS_IN_DAY
from repo.data.git_data import (
    GitData,
    PullRequestData,
    CommitData,
    ContributorData,
    PopularityData,
)
from repo.data.grade import Grade
from repo.services.grade_calculator_service import calculate_grade


@pytest.fixture
def base_git_data():
    return GitData(
        # code=CodeData(
        #     lines_of_code=10_000,
        #     file_count=5000,  # Average file 200 lines long,
        # ),
        pull_request=PullRequestData(
            count=52 * 10,  # One per week for 10 years
            count_open=0,
        ),
        # commit_all=CommitData(
        #     count=52 * 3 * 10,  # Three per week for 10 years
        #     count_primary_author=52 * 3 * 10,
        #     interval=Statistics(
        #         mean=SECONDS_IN_DAY * 5,
        #         standard_deviation=SECONDS_IN_DAY,
        #     ),
        # ),
        commit_recent=CommitData(
            count=6 * 4 * 3,  # 3 per week for 6 months
            count_primary_author=6 * 4 * 3,
            interval=Statistics(
                mean=SECONDS_IN_DAY * 5,
                standard_deviation=SECONDS_IN_DAY,
            ),
        ),
        contributor=ContributorData(
            days_since_create=365 * 10,
            days_since_commit=0,
            # author_count_all=100,
            author_count_recent=100,
        ),
        popularity=PopularityData(watcher_count=100, open_issue_count=0),
    )


def test_perfect_grade(base_git_data: GitData):
    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.A


def test_grade_a(base_git_data: GitData):
    base_git_data.contributor.days_since_create = 1200
    base_git_data.contributor.days_since_commit = 15
    base_git_data.contributor.author_count_all = 30
    base_git_data.contributor.author_count_recent = 10

    # base_git_data.commit_all.count_primary_author = int(52 * 3 * 10 * 0.30)
    base_git_data.commit_recent.count_primary_author = int(6 * 4 * 3 * 0.50)

    # base_git_data.commit_all.interval = Statistics(
    #     mean=SECONDS_IN_DAY * 10,
    #     standard_deviation=SECONDS_IN_DAY,
    # )
    base_git_data.commit_recent.interval = Statistics(
        mean=SECONDS_IN_DAY * 10,
        standard_deviation=SECONDS_IN_DAY,
    )

    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.A


def test_grade_b(base_git_data: GitData):
    base_git_data.contributor.days_since_create = 1000
    base_git_data.contributor.days_since_commit = 45
    base_git_data.contributor.author_count_all = 15
    base_git_data.contributor.author_count_recent = 7

    # base_git_data.commit_all.count_primary_author = int(52 * 3 * 10 * 0.15)
    base_git_data.commit_recent.count_primary_author = int(6 * 4 * 3 * 0.30)

    # base_git_data.commit_all.interval = Statistics(
    #     mean=SECONDS_IN_DAY * 20,
    #     standard_deviation=SECONDS_IN_DAY * 5,
    # )
    base_git_data.commit_recent.interval = Statistics(
        mean=SECONDS_IN_DAY * 20,
        standard_deviation=SECONDS_IN_DAY * 5,
    )

    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.B


def test_grade_c(base_git_data: GitData):
    base_git_data.contributor.days_since_create = 400
    base_git_data.contributor.days_since_commit = 75
    base_git_data.contributor.author_count_all = 5
    base_git_data.contributor.author_count_recent = 4

    # base_git_data.commit_all.count_primary_author = int(52 * 3 * 10 * 0.08)
    base_git_data.commit_recent.count_primary_author = int(6 * 4 * 3 * 0.15)

    # base_git_data.commit_all.interval = Statistics(
    #     mean=SECONDS_IN_DAY * 40,
    #     standard_deviation=SECONDS_IN_DAY * 10,
    # )
    base_git_data.commit_recent.interval = Statistics(
        mean=SECONDS_IN_DAY * 40,
        standard_deviation=SECONDS_IN_DAY * 10,
    )

    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.C


def test_grade_d(base_git_data: GitData):
    base_git_data.contributor.days_since_create = 200
    base_git_data.contributor.days_since_commit = 100
    base_git_data.contributor.author_count_all = 2
    base_git_data.contributor.author_count_recent = 2

    # base_git_data.commit_all.count_primary_author = int(52 * 3 * 10 * 0.04)
    base_git_data.commit_recent.count_primary_author = int(6 * 4 * 3 * 0.08)

    # base_git_data.commit_all.interval = Statistics(
    #     mean=SECONDS_IN_DAY * 75,
    #     standard_deviation=SECONDS_IN_DAY * 10,
    # )
    base_git_data.commit_recent.interval = Statistics(
        mean=SECONDS_IN_DAY * 75,
        standard_deviation=SECONDS_IN_DAY * 10,
    )

    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.D


def test_grade_f(base_git_data: GitData):
    base_git_data.contributor.days_since_create = 100
    base_git_data.contributor.days_since_commit = 400
    base_git_data.contributor.author_count_all = 1
    base_git_data.contributor.author_count_recent = 0

    # base_git_data.commit_all.count_primary_author = int(52 * 3 * 10 * 0.02)
    base_git_data.commit_recent.count_primary_author = int(6 * 4 * 3 * 0.04)

    # base_git_data.commit_all.interval = Statistics(
    #     mean=SECONDS_IN_DAY * 100,
    #     standard_deviation=SECONDS_IN_DAY * 25,
    # )
    base_git_data.commit_recent.interval = Statistics(
        mean=SECONDS_IN_DAY * 100,
        standard_deviation=SECONDS_IN_DAY * 25,
    )

    assert calculate_grade(base_git_data).final_grade.letter_grade == Grade.F
