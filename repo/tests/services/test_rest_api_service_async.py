# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,
import json
import logging
from typing import Any, Generator
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import web
from aiohttp.abc import StreamResponse, Request
from freezegun import freeze_time

from repo.data.from_source import DataFromAPI, TimeData
from repo.data.general import RepoRequest, Statistics, SECONDS_IN_DAY
from repo.services import rest_api_service_async
from repo.tests import github_data
from repo.tests.github_data import COMMITS_PAGE_OBJECTS

logger = logging.getLogger(__name__)


@pytest.fixture
def commit_page_client_response() -> AsyncMock:
    mock_client_response = AsyncMock()
    mock_client_response.json.return_value = github_data.COMMITS_PAGE_RAW
    return mock_client_response


@pytest.mark.asyncio
async def test_extract_commit_list(commit_page_client_response: AsyncMock) -> None:
    actual = await rest_api_service_async._extract_commit_list(commit_page_client_response)  # pylint: disable=protected-access
    assert actual == COMMITS_PAGE_OBJECTS


async def get_repo(request: Request) -> StreamResponse:
    return web.Response(
        body=json.dumps(
            {
                "id": 1,
                "name": "test",
                "created_at": "2019-05-06T00:00:00Z",
                "updated_at": "2022-01-20T00:00:00Z",
                "language": "python",
                "open_issues_count": 10,
                "watchers_count": 1000,
                "forks_count": 10,
            },
        ),
        headers={"content-type": "application/json"},
        status=200,
    )


async def get_pull_request(request: Request) -> StreamResponse:
    if request.url.query.get("state") == "open":
        headers = {
            "link": '<https://api.github.com/repositories/1/pulls?per_page=1&state=all&page=2>; rel="next",'
            " "
            '<https://api.github.com/repositories/1/pulls?per_page=1&state=all&page=10>; rel="last"'
        }
    elif request.url.query.get("state") == "all":
        headers = {
            "link": '<https://api.github.com/repositories/1/pulls?per_page=1&state=all&page=2>; rel="next",'
            " "
            '<https://api.github.com/repositories/1/pulls?per_page=1&state=all&page=100>; rel="last"'
        }
    else:
        raise Exception(f"Invalid pull request state requested: {request.url.query.get('state')}")

    return web.Response(body="", headers=headers, status=200)


async def get_commits(request: Request) -> StreamResponse:
    return web.Response(
        body=json.dumps(
            [
                {"commit": {"author": {"name": "test-name", "date": "2022-01-20T00:00:00Z"}, "message": "commits_back: 0", "comment_count": 0}},
                {"commit": {"author": {"name": "test-name", "date": "2022-01-19T00:00:00Z"}, "message": "commits_back: 1", "comment_count": 0}},
            ]
        ),
        headers={
            "content-type": "application/json",
            "link": "<https://api.github.com/repositories/1/commits?per_page=2&since=2022-01-20T00%3A00%3A00Z&page=2>; "
            'rel="next",'
            " "
            "<https://api.github.com/repositories/1/commits?per_page=2&since=2022-01-20T00%3A00%3A00Z&page=5>; "
            'rel="last"',
        },
        status=200,
    )


async def get_paginated_commits(request: Request) -> StreamResponse:
    page = request.url.query.get("page")
    logger.debug("  page: %s", page)
    commit_counter = (int(page if page else 2) - 1) * 2
    return web.Response(
        body=json.dumps(
            [
                {"commit": {"author": {"name": "test-name", "date": f"2022-01-{20 - commit_counter}T00:00:00Z"}, "message": f"commits_back: {commit_counter}", "comment_count": 0}},
                {
                    "commit": {
                        "author": {"name": "test-name", "date": f"2022-01-{20 - commit_counter - 1}T00:00:00Z"},
                        "message": f"commits_back: {commit_counter + 1}",
                        "comment_count": 0,
                    }
                },
            ]
        ),
        headers={"content-type": "application/json"},
        status=200,
    )


async def get_tag(request: Request) -> StreamResponse:
    # The sha is hacked to be a mock hash with the last digit being a sequential int
    sha: str = request.match_info["sha"]
    int_hack = int(sha[-1]) + 1

    tag = {"tag": f"{int_hack}.0.0", "tagger": {"date": f"2022-01-{10 + int_hack}T00:00:00Z"}}

    return web.Response(body=json.dumps(tag), headers={"content-type": "application/json"}, status=200)


async def get_tags(request: Request) -> StreamResponse:
    tags = [{"object": {"sha": f"abcdefg{i}"}} for i in range(10, 0, -1)]

    return web.Response(
        body=json.dumps(tags),
        headers={"content-type": "application/json"},
        status=200,
    )


@pytest.fixture
def patched_aiohttp_client(loop, aiohttp_client: AsyncMock) -> Any:
    github_stub = web.Application()
    github_stub.router.add_get("/repos/test/test", get_repo)
    github_stub.router.add_get("/repos/test/test/pulls", get_pull_request)

    github_stub.router.add_get("/repos/test/test/commits", get_commits)
    github_stub.router.add_get("/repositories/1/commits", get_paginated_commits)

    github_stub.router.add_get("/repos/test/test/git/matching-refs/tags", get_tags)
    github_stub.router.add_get("/repos/test/test/git/tags/{sha}", get_tag)

    return loop.run_until_complete(aiohttp_client(github_stub))


@pytest.fixture
def disable_sleep() -> Generator[None, None, None]:
    with patch("repo.services.rest_api_service_async.asyncio.sleep"):
        yield


@pytest.mark.asyncio
@freeze_time("2022-01-30")
async def test_fetch_github(patched_aiohttp_client: Any, disable_sleep: None) -> None:
    with patch("repo.services.rest_api_service_async.aiohttp.ClientSession") as mock_client_session:
        mock_client_session.return_value.__aenter__.return_value = patched_aiohttp_client

        source = RepoRequest(source="test", owner="test", repo="test")
        actual = await rest_api_service_async.fetch_github_api_data(source)
        expected = DataFromAPI(
            days_since_update=10,
            days_since_create=1000,
            watcher_count=1000,
            pull_request_count_open=10,
            pull_request_count=100,
            open_issue_count=10,
            days_since_commit=10,
            time_recent=TimeData(
                commit_count=10,
                commit_count_primary_author=10,
                commit_interval=Statistics(mean=float(SECONDS_IN_DAY), standard_deviation=0.0),
                author_count=1,
            ),
            latest_release="10.0.0",
            releases_count=10,
            days_since_last_release=10,
        )
    assert actual == expected
