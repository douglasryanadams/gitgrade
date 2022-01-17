import copy
from typing import Union, Generator
from unittest.mock import patch, Mock

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from freezegun import freeze_time

from repo.services import (
    SourceMetadata,
    identify_source,
    UnsupportedURL,
    _extract_page_count,
    _fetch_bitbucket,
    ApiBasedData,
)
from repo.tests import bitbucket_objects


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/git/git",
            SourceMetadata(source="github", owner="git", repo="git"),
        ),
        (
            "https://github.com/apache/httpd",
            SourceMetadata(source="github", owner="apache", repo="httpd"),
        ),
        (
            "https://bitbucket.org/atlassian/bamboo-tomcat-plugin/src/master/",
            SourceMetadata(
                source="bitbucket", owner="atlassian", repo="bamboo-tomcat-plugin"
            ),
        ),
        (
            "https://bitbucket.org/schae/test-test-test/src/master/",
            SourceMetadata(source="bitbucket", owner="schae", repo="test-test-test"),
        ),
        (
            "https://opensource.ncsa.illinois.edu/bitbucket/projects/ERGO/repos/tutorial/browse",
            UnsupportedURL,
        ),
        ("https://www.google.com/", UnsupportedURL),
        ("gobbledygook", ValidationError),
    ],
)
def test_identify_source(
    url: str, expected: Union[SourceMetadata, BaseException]
) -> None:
    """
    Should make sure we're parsing repo paths correctly and document our supported/unsupported URL examples
    """
    if isinstance(expected, SourceMetadata):
        actual_metadata = identify_source(url)
        assert actual_metadata == expected
    else:
        with pytest.raises(expected):  # type: ignore
            identify_source(url)


@pytest.mark.parametrize(
    "link_text, expected",
    [
        (
            '<https://api.github.com/repositories/205423/contributors?per_page=1&page=2>; rel="next", '
            '<https://api.github.com/repositories/205423/contributors?per_page=1&page=45>; rel="last"',
            45,
        ),
        (
            '<https://api.github.com/repositories/205423/contributors?per_page=1&page=1>; rel="next", '
            '<https://api.github.com/repositories/205423/contributors?per_page=1&page=1>; rel="last"',
            1,
        ),
        ("invalid", 0),
    ],
)
def test_extract_page_count(link_text: str, expected: int) -> None:
    """
    Make sure we correctly process the link header from github
    """
    actual = _extract_page_count(link_text)
    assert actual == expected


@pytest.fixture
def bitbucket_requests_client() -> Generator[Mock, None, None]:
    """
    Stubs out responses for bitbucket calls to avoid real network calls
    """
    with patch("repo.services.requests") as mock_requests:
        mock_repo_response = Mock()
        mock_repo_response.json.return_value = copy.deepcopy(bitbucket_objects.REPO)

        mock_watchers_response = Mock()
        mock_watchers_response.json.return_value = copy.deepcopy(
            bitbucket_objects.WATCHERS
        )

        mock_open_prs_response = Mock()
        mock_open_prs_response.json.return_value = copy.deepcopy(
            bitbucket_objects.OPEN_PRS
        )

        mock_all_prs_response = Mock()
        mock_all_prs_response.json.return_value = copy.deepcopy(
            bitbucket_objects.ALL_PRS
        )

        mock_requests.get.side_effect = [
            mock_repo_response,
            mock_watchers_response,
            mock_open_prs_response,
            mock_all_prs_response,
        ]
        yield mock_requests


@freeze_time("2022-01-30")
def test_fetch_bitbucket(bitbucket_requests_client: Mock) -> None:  # pylint: disable=W
    """
    Tests that we parse some sample data successfully

    Note: Careful running this w/o mock data, Bitbucket has very low rate limits
    """
    settings.configure()
    source = SourceMetadata(
        source="bitbucket", owner="atlassian", repo="bamboo-tomcat-plugin"
    )
    actual = _fetch_bitbucket(source)
    expected = ApiBasedData(
        days_since_create=663,
        days_since_update=307,
        watchers=2,
        pull_requests_open=0,
        pull_requests_total=1,
        has_issues=False,
        open_issues=-1,
        github_data=None,
    )
    assert actual == expected
