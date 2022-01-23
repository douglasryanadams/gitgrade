# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import copy
from datetime import datetime
from typing import Generator
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time

from repo.services.rest_api_service import (
    _fetch_bitbucket_api_data,
    _fetch_github_api_data,
)
from repo.services.data import UrlMetadata, ApiData
from repo.tests import bitbucket_objects


@pytest.fixture
def patch_bitbucket_requests() -> Generator[Mock, None, None]:
    """
    Stubs out responses for bitbucket calls to avoid real network calls
    """
    with patch("repo.services.rest_api_service.requests") as mock_requests:
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
    with patch("repo.services.rest_api_service.Github") as mock_constructor:
        mock_client = Mock()
        mock_constructor.return_value = mock_client

        mock_repo = Mock()
        mock_repo.updated_at = datetime(2022, 1, 16, 22, 28, 41)
        mock_repo.created_at = datetime(2008, 7, 23, 14, 21, 26)
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
