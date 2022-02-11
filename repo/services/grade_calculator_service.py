# pylint: disable=too-many-return-statements, too-few-public-methods

import logging

from repo.services.data import ApiData, LocalData, Grade, TestGrades

logger = logging.getLogger(__name__)


class DaysSinceCommit:
    """
    Scores based on how long it's been since the last commit.
    Encourages frequent maintenance to codebase.

    Tensions:
        - RepoAge
    """

    max_score = 200

    @classmethod
    def get_score(cls, days_since_commit: int) -> float:
        if days_since_commit > 365 * 2:
            return 0
        if days_since_commit > 365:
            return cls.max_score * 0.5
        if days_since_commit > 182:
            return cls.max_score * 0.6
        if days_since_commit > 91:
            return cls.max_score * 0.7
        if days_since_commit > 60:
            return cls.max_score * 0.8
        if days_since_commit > 30:
            return cls.max_score * 0.9
        return cls.max_score


class RepoAge:
    """
    Scores repo based on how long it's been around.
    Encourages using older well tested codebases.

    Tensions:
        - DaysSinceCommit
    """

    max_score = 100

    @classmethod
    def get_score(cls, days_since_create: int) -> float:
        if days_since_create > 365 * 4:
            return cls.max_score
        if days_since_create > 365 * 3:
            return cls.max_score * 0.9
        if days_since_create > 365 * 2:
            return cls.max_score * 0.8
        if days_since_create > 365:
            return cls.max_score * 0.7
        if days_since_create > 182:
            return cls.max_score * 0.6
        if days_since_create > 90:
            return cls.max_score * 0.5
        return 0


class TotalAuthors:
    """
    Scores repo based on how many contributors have helped
    Encourages redundant maintainers and knowledge duplication

    Tensions:
        - Total Prolific Authors
        - Recent Authors
    """

    max_score = 100

    @classmethod
    def get_score(cls, authors_total: int) -> float:
        if authors_total > 50:
            return cls.max_score
        if authors_total > 25:
            return cls.max_score * 0.9
        if authors_total > 10:
            return cls.max_score * 0.8
        if authors_total > 3:
            return cls.max_score * 0.7
        if authors_total > 1:
            return cls.max_score * 0.6
        if authors_total > 0:
            return cls.max_score * 0.5
        return 0  # Only really possible if the only author abandoned the platform


class RecentAuthors:
    """
    Scores repo based on recent contributors
    Encourages retaining active contributions from diverse perspectives

    Tensions:
        - Recent Prolific Authors
        - Total Authors
    """

    max_score = 150

    @classmethod
    def get_score(cls, authors_recent: int) -> float:
        if authors_recent > 10:
            return cls.max_score
        if authors_recent > 5:
            return cls.max_score * 0.9
        if authors_recent > 3:
            return cls.max_score * 0.8
        if authors_recent > 1:
            return cls.max_score * 0.7
        return cls.max_score * 0.5


class TotalProlificAuthors:
    """
    Scores repo based percentage of contributions from single author
    Encourages having a leader for the project

    Tensions:
        - Total Authors
    """

    max_score = 100

    @classmethod
    def get_score(cls, total_commits: int, prolific_author_commits: int) -> float:
        if total_commits == 0:
            # If somehow there have been no commits, return a neutral "C"
            return cls.max_score * 0.75

        logger.debug(
            "  TotalProlificAuthors (%s/%s): %s",
            prolific_author_commits,
            total_commits,
            prolific_author_commits / total_commits,
        )

        if prolific_author_commits / total_commits > 0.25:
            return cls.max_score
        if prolific_author_commits / total_commits > 0.10:
            return cls.max_score * 0.9
        if prolific_author_commits / total_commits > 0.05:
            return cls.max_score * 0.8
        if prolific_author_commits / total_commits > 0.025:
            return cls.max_score * 0.7
        if prolific_author_commits / total_commits > 0.01:
            return cls.max_score * 0.6

        return cls.max_score * 0.5


class RecentProlificAuthors:
    """
    Scores repo based percentage of contributions from single author
    Encourages having a leader for the project

    Tensions:
        - Recent Authors
    """

    max_score = 100

    @classmethod
    def get_score(cls, total_commits: int, prolific_author_commits: int) -> float:
        if total_commits == 0:
            return cls.max_score * 0.75

        logger.debug(
            "  RecentProlificAuthors (%s/%s): %s",
            prolific_author_commits,
            total_commits,
            prolific_author_commits / total_commits,
        )

        if prolific_author_commits / total_commits > 0.40:
            return cls.max_score
        if prolific_author_commits / total_commits > 0.25:
            return cls.max_score * 0.9
        if prolific_author_commits / total_commits > 0.10:
            return cls.max_score * 0.8
        if prolific_author_commits / total_commits > 0.05:
            return cls.max_score * 0.7
        if prolific_author_commits / total_commits > 0.025:
            return cls.max_score * 0.6

        return cls.max_score * 0.25


def _get_letter_grade(score: float, total_max_score: float) -> Grade:
    score = score / total_max_score
    if score > 0.9:
        return Grade.A
    if score > 0.8:
        return Grade.B
    if score > 0.7:
        return Grade.C
    if score > 0.6:
        return Grade.D
    return Grade.F


def calculate_grade(api_data: ApiData, local_data: LocalData) -> TestGrades:
    """
    This method calculates a grade for the repo using a similar system to
    American public schools (for better or worse). Each metric is a "test"
    that results in an individual score. Some "tests" are worth more than
    others.
    """
    logger.info("Calculating grade")
    logger.debug("  api_data: %s", api_data)
    logger.debug("  local_data: %s", local_data)

    days_since_commit = DaysSinceCommit.get_score(local_data.days_since_commit)
    repo_age = RepoAge.get_score(api_data.days_since_create)
    total_authors = TotalAuthors.get_score(local_data.authors_total)
    recent_authors = RecentAuthors.get_score(local_data.authors_recent)
    total_prolific_authors = TotalProlificAuthors.get_score(
        local_data.commits_total, local_data.prolific_author_commits_total
    )
    recent_prolific_authors = RecentProlificAuthors.get_score(
        local_data.commits_recent, local_data.prolific_author_commits_recent
    )

    total_max_score = sum(
        [
            DaysSinceCommit.max_score,
            RepoAge.max_score,
            TotalAuthors.max_score,
            RecentAuthors.max_score,
            TotalProlificAuthors.max_score,
            RecentProlificAuthors.max_score,
        ]
    )

    repo_final_score = sum(
        [
            days_since_commit,
            repo_age,
            total_authors,
            recent_authors,
            total_prolific_authors,
            recent_prolific_authors,
        ]
    )

    return TestGrades(
        days_since_commit=_get_letter_grade(
            days_since_commit, DaysSinceCommit.max_score
        ),
        repo_age=_get_letter_grade(repo_age, RepoAge.max_score),
        total_authors=_get_letter_grade(total_authors, TotalAuthors.max_score),
        recent_authors=_get_letter_grade(recent_authors, RecentAuthors.max_score),
        total_prolific_authors=_get_letter_grade(
            total_prolific_authors, TotalProlificAuthors.max_score
        ),
        recent_prolific_authors=_get_letter_grade(
            recent_prolific_authors, RecentProlificAuthors.max_score
        ),
        final_grade=_get_letter_grade(repo_final_score, total_max_score),
    )
