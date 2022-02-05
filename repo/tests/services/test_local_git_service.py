# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import json
from datetime import datetime
from typing import Generator
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time

from repo.services.data import RepoRequestData, LocalData
from repo.services.local_git_service import fetch_local_data


@pytest.fixture
def mock_os() -> Generator[Mock, None, None]:
    with patch("repo.services.local_git_service.os") as mock:
        mock.path.exists.return_value = True
        yield mock


@pytest.fixture
def mock_shutil() -> Generator[Mock, None, None]:
    with patch("repo.services.local_git_service.shutil") as mock:
        yield mock


@pytest.fixture
def mock_commit() -> Generator[Mock, None, None]:
    commit = Mock()
    commit.committed_date = int(
        (datetime(2022, 1, 20) - datetime(1970, 1, 1)).total_seconds()
    )
    return commit


@pytest.fixture
def mock_gitpython(mock_commit) -> Generator[Mock, None, None]:
    with patch("repo.services.local_git_service.Repo") as mock:
        repo = Mock()
        mock.return_value = repo
        # mock.clone_from.return_value = repo

        repo.remotes = {"origin": Mock()}

        repo.git.ls_remote.return_value = (
            "b56bd95bbc8f716cb8cbb5fdc18b9b0f00323c6a\trefs/heads/master\n"
            "b56bd95bbc8f716cb8cbb5fdc18b9b0f00323c6a\trefs/heads/main"
        )
        repo.git.shortlog.side_effect = [
            " 400\tAuthor Alpha\n 25\tAuthor Beta\n 25\tAuthor Gamma\n 25\tAuthor Delta\n 25\tAuthor Epsilon",
            " 80\tAuthor Alpha\n 20\tAuthor Beta",
        ]

        repo.head.commit = mock_commit

        yield mock


@pytest.fixture
def mock_subprocess() -> Generator[Mock, None, None]:
    with patch("repo.services.local_git_service.subprocess") as mock:
        cloc = Mock()

        mock.run.side_effect = [None, cloc]

        cloc.stdout = json.dumps({"SUM": {"code": 1000, "nFiles": 10}})

        yield mock


@freeze_time("2022-01-30")
def test_fetch_local_data(
    mock_os: Mock, mock_shutil: Mock, mock_gitpython: Mock, mock_subprocess: Mock
) -> None:
    url_data = RepoRequestData(source="github", owner="git", repo="git")
    actual = fetch_local_data(url_data)

    expected = LocalData(
        days_since_commit=10,
        commits_total=500,
        commits_recent=100,
        branch_count=2,
        authors_total=5,
        authors_recent=2,
        prolific_author_commits_total=400,
        prolific_author_commits_recent=80,
        lines_of_code_total=1000,
        files_total=10,
    )

    assert actual == expected
    mock_shutil.rmtree.assert_called_with("/tmp/gitgrade/github_git_git")
