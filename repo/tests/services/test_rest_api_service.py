# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

from datetime import datetime
from typing import Generator, List
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time

from repo.data.from_source import DataFromAPI, TimeData
from repo.data.general import RepoRequest, Statistics, SECONDS_IN_DAY

from repo.services.rest_api_service import fetch_github_api_data


@pytest.fixture
def mock_commits() -> List[Mock]:
    commits = []
    for i in range(10):
        mock_commit = Mock()
        commits.append(mock_commit)
        mock_author = Mock()
        mock_author.name = "userA"
        mock_author.date = datetime(2022, 1, 10 - i)  # one commit per day
        mock_commit.commit.author = mock_author
    return commits


@pytest.fixture
def patch_github_client(mock_commits) -> Generator[Mock, None, None]:
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

        mock_repo.get_commits.return_value = mock_commits
        mock_branches_response = Mock()
        mock_branches_response.totalCount = 2
        mock_repo.get_branches.return_value = mock_branches_response

        yield mock_constructor


@freeze_time("2022-01-30")
def test_fetch_github(patch_github_client: Mock) -> None:
    source = RepoRequest(source="github", owner="git", repo="git")
    actual = fetch_github_api_data(source)
    expected = DataFromAPI(
        days_since_update=14,
        days_since_create=4939,
        watcher_count=40736,
        pull_request_count_open=86,
        pull_request_count=1016,
        has_issues=False,
        open_issue_count=93,
        days_since_commit=20,
        branch_count=2,
        time_recent=TimeData(
            commit_count=10,
            commit_count_primary_author=10,
            commit_interval=Statistics(
                mean=float(SECONDS_IN_DAY), standard_deviation=0.0
            ),
            author_count=1,
        ),
    )
    assert actual == expected
