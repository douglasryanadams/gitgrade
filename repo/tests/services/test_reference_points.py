import logging

import pytest

from repo.services.data import Grade
from repo.services.repo_input_service import repo_input_util

logger = logging.getLogger(__name__)


@pytest.mark.integration_test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url, expected_grade",
    [
        ("https://github.com/apache/httpd", Grade.A),
        ("https://github.com/rails/rails", Grade.A),
        ("https://github.com/microsoft/TypeScript", Grade.A),
        ("https://github.com/tiangolo/fastapi", Grade.A),
        ("https://github.com/projectdiscovery/httpx", Grade.B),
        ("https://github.com/postmanlabs/httpbin", Grade.F),
    ],
)
def test_baselines(
    url: str,
    expected_grade: Grade,
) -> None:
    """
    This is a gut-check that we're in the ball-park with our grading logic.
    I considered making this a "snapshot" of these repos but that posed
    some problems keeping that data up to date would be painful. I also wanted
    to make sure that new metrics kept these grades relatively stable. With
    canned data, we'd not only need to update every time we update grading, but
    we would also have to update all of them every time we add new metrics.

    This also ensures that the app still works end-to-end (mostly).

    Finally, this test will encourage optimizing the evaluation speed of repos because
    we're doing a few "for real."
    """
    response_json = repo_input_util(url)
    logger.debug("response_json=%s", response_json)
    assert response_json["grades"]["final_grade"]["letter_grade"] == expected_grade
