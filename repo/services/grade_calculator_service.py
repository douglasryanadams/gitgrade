# pylint: disable=too-many-return-statements, too-few-public-methods

import logging

from repo.services.data import ApiData, LocalData, Grade

logger = logging.getLogger(__name__)


class DaysSinceCommit:
    max_score = 100

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


def calculate_grade(api_data: ApiData, local_data: LocalData) -> Grade:
    """
    This method calculates a grade for the repo using a similar system to
    American public schools (for better or worse). Each metric is a "test"
    that results in an individual score. Some "tests" are worth more than
    others.
    """
    logger.info("Calculating grade")
    logger.debug("  api_data: %s", api_data)
    logger.debug("  local_data: %s", local_data)

    total_max_score = sum((DaysSinceCommit.max_score,))

    repo_final_score = sum((DaysSinceCommit.get_score(local_data.days_since_commit),))

    score = repo_final_score / total_max_score

    if score > 0.9:
        return Grade.A
    if score > 0.8:
        return Grade.B
    if score > 0.7:
        return Grade.C
    if score > 0.6:
        return Grade.D

    return Grade.F
