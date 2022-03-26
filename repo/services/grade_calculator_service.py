# pylint: disable=too-many-return-statements, too-few-public-methods

import logging
from typing import Union, Optional

from repo.data.general import Statistics, SECONDS_IN_DAY
from repo.data.git_data import GitData
from repo.data.grade import TestGrade, TestGrades, Grade

logger = logging.getLogger(__name__)


def _construct_grade(
    points_max: float,
    points_earned: float,
    raw_number: Union[int, float],
    unit: Optional[str] = None,
) -> TestGrade:
    score = points_earned / points_max

    if score > 0.9:
        letter_grade = Grade.A
    elif score > 0.8:
        letter_grade = Grade.B
    elif score > 0.7:
        letter_grade = Grade.C
    elif score > 0.6:
        letter_grade = Grade.D
    else:
        letter_grade = Grade.F

    weight = points_max / 100
    return TestGrade(
        letter_grade=letter_grade,
        points_max=points_max,
        points_earned=points_earned,
        weight=points_max / 100,
        weight_str=f"{weight:.2f}",
        raw_number=raw_number,
        unit=unit,
    )


def grade_days_since_commit(days_since_commit: int) -> TestGrade:
    """
    Scores based on how long it's been since the last commit.
    Encourages frequent maintenance to codebase.

    Tensions:
        - Repo Age
    """
    points_max = 200.0

    if days_since_commit > 365 * 2:
        points_earned = 0.0
    elif days_since_commit > 365:
        points_earned = points_max * 0.5
    elif days_since_commit > 182:
        points_earned = points_max * 0.6
    elif days_since_commit > 91:
        points_earned = points_max * 0.7
    elif days_since_commit > 60:
        points_earned = points_max * 0.8
    elif days_since_commit > 30:
        points_earned = points_max * 0.9
    else:
        points_earned = points_max

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=days_since_commit,
        unit="Days",
    )


def grade_days_since_create(days_since_create: int) -> TestGrade:
    """
    Scores repo based on how long it's been around.
    Encourages using older well tested code bases.

    Tensions:
        - DaysSinceCommit
        - CommitInterval
    """
    points_max = 125.0

    if days_since_create > 365 * 4:
        points_earned = points_max
    elif days_since_create > 365 * 3:
        points_earned = points_max * 0.9
    elif days_since_create > 365 * 2:
        points_earned = points_max * 0.8
    elif days_since_create > 365:
        points_earned = points_max * 0.7
    elif days_since_create > 182:
        points_earned = points_max * 0.6
    elif days_since_create > 90:
        points_earned = points_max * 0.5
    else:
        points_earned = 0.0

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=days_since_create,
        unit="Days",
    )


def grade_authors_total(authors_total: int) -> TestGrade:
    """
    Scores repo based on how many contributors have helped
    Encourages redundant maintainers and knowledge duplication

    Tensions:
        - Total Prolific Authors
        - Recent Authors
    """
    points_max = 100.0

    if authors_total > 50:
        points_earned = points_max
    elif authors_total > 25:
        points_earned = points_max * 0.9
    elif authors_total > 10:
        points_earned = points_max * 0.8
    elif authors_total > 3:
        points_earned = points_max * 0.7
    elif authors_total > 1:
        points_earned = points_max * 0.6
    elif authors_total > 0:
        points_earned = points_max * 0.5
    else:
        points_earned = 0.0

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=authors_total,
        unit="Authors",
    )


def grade_authors_recent(authors_recent: int) -> TestGrade:
    """
    Scores repo based on recent contributors
    Encourages retaining active contributions from diverse perspectives

    Tensions:
        - Recent Prolific Authors
        - Total Authors
    """
    points_max = 150.0

    if authors_recent > 10:
        points_earned = points_max
    elif authors_recent > 5:
        points_earned = points_max * 0.9
    elif authors_recent > 3:
        points_earned = points_max * 0.8
    elif authors_recent > 1:
        points_earned = points_max * 0.7
    else:
        points_earned = points_max * 0.5

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=authors_recent,
        unit="Authors",
    )


def grade_commits_all_by_primary_author(total_commits: int, primary_author_commits: int) -> TestGrade:
    """
    Scores repo based percentage of contributions from single author
    Encourages having a leader for the project

    Tensions:
        - Total Authors
    """
    points_max = 100
    if total_commits == 0:
        # If somehow there have been no commits, return a neutral "C"
        points_earned = points_max * 0.75
    else:
        logger.debug(
            "  TotalProlificAuthors (%s/%s): %s",
            primary_author_commits,
            total_commits,
            primary_author_commits / total_commits,
        )

        if primary_author_commits / total_commits > 0.25:
            points_earned = points_max
        elif primary_author_commits / total_commits > 0.10:
            points_earned = points_max * 0.9
        elif primary_author_commits / total_commits > 0.05:
            points_earned = points_max * 0.8
        elif primary_author_commits / total_commits > 0.025:
            points_earned = points_max * 0.7
        elif primary_author_commits / total_commits > 0.01:
            points_earned = points_max * 0.6
        else:
            points_earned = points_max * 0.5

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=round(100 * (primary_author_commits / total_commits), 2),
        unit="Percent",
    )


def grade_commits_recent_by_primary_author(total_commits: int, primary_author_commits: int) -> TestGrade:
    """
    Scores repo based percentage of contributions from single author
    Encourages having a leader for the project

    Tensions:
        - Recent Authors
    """
    points_max = 100
    if total_commits == 0:
        points_earned = points_max * 0.50
    else:
        logger.debug(
            "  RecentProlificAuthors (%s/%s): %s",
            primary_author_commits,
            total_commits,
            primary_author_commits / total_commits,
        )

        if primary_author_commits / total_commits > 0.40:
            points_earned = points_max
        elif primary_author_commits / total_commits > 0.25:
            points_earned = points_max * 0.9
        elif primary_author_commits / total_commits > 0.10:
            points_earned = points_max * 0.8
        elif primary_author_commits / total_commits > 0.05:
            points_earned = points_max * 0.7
        elif primary_author_commits / total_commits > 0.025:
            points_earned = points_max * 0.6
        else:
            points_earned = points_max * 0.25

    if total_commits:
        raw_number = round(100 * (primary_author_commits / total_commits), 2)
    else:
        raw_number = 0

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=raw_number,
        unit="Percent",
    )


def grade_commit_interval(commit_stats: Statistics) -> TestGrade:
    """
    Scores repo based on 1 std deviation above the mean of time between commits

    Tensions:
        - RepoAge
    """
    points_max = 100.0
    majority = commit_stats.majority

    if majority == 0:  # Implies that there's no activity at all
        points_earned = 0.0
    elif majority < (SECONDS_IN_DAY * 7):
        points_earned = points_max
    elif majority < (SECONDS_IN_DAY * 14):
        points_earned = points_max * 0.9
    elif majority < (SECONDS_IN_DAY * 28):
        points_earned = points_max * 0.8
    elif majority < (SECONDS_IN_DAY * 60):
        points_earned = points_max * 0.7
    elif majority < (SECONDS_IN_DAY * 90):
        points_earned = points_max * 0.6
    else:
        points_earned = points_max * 0.5

    return _construct_grade(
        points_max=points_max,
        points_earned=points_earned,
        raw_number=round(majority / SECONDS_IN_DAY, 2),
        unit="Days",
    )


def calculate_grade(data: GitData) -> TestGrades:
    """
    This method calculates a grade for the repo using a similar system to
    American public schools (for better or worse). Each metric is a "test"
    that results in an individual score. Some "tests" are worth more than
    others.
    """
    logger.info("Calculating grade")
    logger.debug("  data: %s", data)

    test_grades = {
        "days_since_commit": grade_days_since_commit(data.contributor.days_since_commit),
        "days_since_create": grade_days_since_create(data.contributor.days_since_create),
        # "author_count_all": grade_authors_total(data.contributor.author_count_all),
        "author_count_recent": grade_authors_recent(data.contributor.author_count_recent),
        # "commit_count_primary_author_all": grade_commits_all_by_primary_author(
        #     data.commit_all.count,
        #     data.commit_all.count_primary_author,
        # ),
        "commit_count_primary_author_recent": grade_commits_recent_by_primary_author(
            data.commit_recent.count,
            data.commit_recent.count_primary_author,
        ),
        # "commit_interval_all": grade_commit_interval(data.commit_all.interval),
        "commit_interval_recent": grade_commit_interval(data.commit_recent.interval),
    }

    final_points_max = sum([grade.points_max for grade in test_grades.values()])
    final_points_earned = sum([grade.points_earned for grade in test_grades.values()])
    final_grade = _construct_grade(
        points_max=final_points_max,
        points_earned=final_points_earned,
        raw_number=round(100 * (final_points_earned / final_points_max), 2),
        unit="Percent",
    )

    return TestGrades(final_grade=final_grade, **test_grades)
