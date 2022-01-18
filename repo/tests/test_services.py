# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import copy
import datetime
import json
from typing import Union, Generator
from unittest.mock import patch, Mock

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from freezegun import freeze_time

from repo.services import (
    UrlMetadata,
    identify_source,
    UnsupportedURL,
    _fetch_bitbucket_api_data,
    ApiData,
    _fetch_github_api_data,
    fetch_local_data,
    LocalData,
)
from repo.tests import bitbucket_objects


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/git/git",
            UrlMetadata(source="github", owner="git", repo="git"),
        ),
        (
            "https://github.com/apache/httpd",
            UrlMetadata(source="github", owner="apache", repo="httpd"),
        ),
        (
            "https://bitbucket.org/atlassian/bamboo-tomcat-plugin/src/master/",
            UrlMetadata(
                source="bitbucket", owner="atlassian", repo="bamboo-tomcat-plugin"
            ),
        ),
        (
            "https://bitbucket.org/schae/test-test-test/src/master/",
            UrlMetadata(source="bitbucket", owner="schae", repo="test-test-test"),
        ),
        (
            "https://opensource.ncsa.illinois.edu/bitbucket/projects/ERGO/repos/tutorial/browse",
            UnsupportedURL,
        ),
        ("https://www.google.com/", UnsupportedURL),
        ("gobbledygook", ValidationError),
    ],
)
def test_identify_source(url: str, expected: Union[UrlMetadata, BaseException]) -> None:
    """
    Should make sure we're parsing repo paths correctly and document our supported/unsupported URL examples
    """
    if isinstance(expected, UrlMetadata):
        actual_metadata = identify_source(url)
        assert actual_metadata == expected
    else:
        with pytest.raises(expected):  # type: ignore
            identify_source(url)


@pytest.fixture
def patch_bitbucket_requests() -> Generator[Mock, None, None]:
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
def test_fetch_bitbucket(patch_bitbucket_requests: Mock) -> None:  # pylint: disable=W
    """
    Tests that we parse some sample data successfully

    Note: Careful running this w/o mock data, Bitbucket has very low rate limits
    """
    settings.configure()
    source = UrlMetadata(
        source="bitbucket", owner="atlassian", repo="bamboo-tomcat-plugin"
    )
    actual = _fetch_bitbucket_api_data(source)
    expected = ApiData(
        days_since_create=663,
        days_since_update=307,
        watchers=2,
        pull_requests_open=0,
        pull_requests_total=1,
        has_issues=False,
        open_issues=-1,
    )
    assert actual == expected


@pytest.fixture
def patch_github_client() -> Generator[Mock, None, None]:
    with patch("repo.services.Github") as mock_constructor:
        mock_client = Mock()
        mock_constructor.return_value = mock_client

        mock_repo = Mock()
        mock_repo.updated_at = datetime.datetime(2022, 1, 16, 22, 28, 41)
        mock_repo.created_at = datetime.datetime(2008, 7, 23, 14, 21, 26)
        mock_repo.watchers_count = 40736
        mock_repo.has_issues = False
        mock_repo.open_issues_count = 93

        mock_open_pulls = Mock()
        mock_open_pulls.totalCount = 86

        mock_all_pulls = Mock()
        mock_all_pulls.totalCount = 1016

        mock_repo.get_pulls.side_effect = [mock_open_pulls, mock_all_pulls]

        mock_client.get_repo.return_value = mock_repo

        yield mock_constructor


@freeze_time("2022-01-30")
def test_fetch_github(patch_github_client: Mock) -> None:
    source = UrlMetadata(source="github", owner="git", repo="git")
    actual = _fetch_github_api_data(source)
    expected = ApiData(
        days_since_create=4939,
        days_since_update=14,
        watchers=40736,
        pull_requests_open=86,
        pull_requests_total=1016,
        has_issues=False,
        open_issues=93,
    )
    assert actual == expected


@pytest.fixture
def mock_os() -> Generator[Mock, None, None]:
    with patch("repo.services.os") as mock:
        mock.path.exists.return_value = True
        yield mock


@pytest.fixture
def mock_gitpython() -> Generator[Mock, None, None]:
    with patch("repo.services.Repo") as mock:
        repo = Mock()
        mock.return_value = repo
        # mock.clone_from.return_value = repo

        repo.remotes = {"origin": Mock()}

        repo.git.ls_remote.return_value = (
            "b56bd95bbc8f716cb8cbb5fdc18b9b0f00323c6a\trefs/heads/master\n"
            "b56bd95bbc8f716cb8cbb5fdc18b9b0f00323c6a\trefs/heads/main"
        )
        repo.git.shortlog.side_effect = [
            " 100\tAuthor Alpha\n 100\tAuthor Beta\n 100\tAuthor Gamma\n 100\tAuthor Delta\n 100\tAuthor Epsilon",
            " 50\tAuthor Alpha\n 50\tAuthor Beta",
        ]

        yield mock


@pytest.fixture
def mock_subprocess() -> Generator[Mock, None, None]:
    with patch("repo.services.subprocess") as mock:
        cloc = Mock()

        mock.run.side_effect = [None, cloc]

        cloc.stdout = json.dumps({"SUM": {"code": 1000, "nFiles": 10}})

        yield mock


@freeze_time("2022-01-30")
def test_fetch_local_data(
    mock_os: Mock, mock_gitpython: Mock, mock_subprocess: Mock
) -> None:
    url_data = UrlMetadata(source="github", owner="git", repo="git")
    actual = fetch_local_data(url_data)

    expected = LocalData(
        commits_total=500,
        commits_recent=100,
        branch_count=2,
        authors_total=5,
        authors_recent=2,
        lines_of_code_total=1000,
        files_total=10,
    )

    assert actual == expected
