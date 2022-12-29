import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Final, Literal

import aiohttp
from aiohttp import ClientSession, ClientResponse
from multidict import MultiDict
from yarl import URL

from repo.data.from_source import DataFromAPI, TimeData
from repo.data.general import RepoRequest, Statistics
from repo.data.github import Repo, Commit, Author, Release
from repo.services.util import get_statistics

logger = logging.getLogger(__name__)

GITHUB_DATETIME_FORMAT: Final = "%Y-%m-%dT%H:%M:%S%z"
BASE_URL: Final = "https://api.github.com"
RECENT_DAYS: Final = 182  # About 6 months


def _github_datestring_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, GITHUB_DATETIME_FORMAT)


def _github_datetime_to_datestring(date: datetime) -> str:
    return date.strftime(GITHUB_DATETIME_FORMAT)


async def _get_repo(uri: str, session: ClientSession) -> Repo:
    logger.debug("  fetching repo: %s", uri)
    async with session.get(f"/repos/{uri}") as repo_response:
        repo_response_json = await repo_response.json()

    repo = Repo(
        id=repo_response_json.get("id", "-1"),
        name=repo_response_json.get("name", "unknown"),
        created_at=repo_response_json.get("created_at", "1970-01-01T00:00:00Z"),
        updated_at=repo_response_json.get("updated_at", "1970-01-01T00:00:00Z"),
        language=repo_response_json.get("language", "unknown"),
        open_issues_count=repo_response_json.get("open_issues_count", "-1"),
        watchers_count=repo_response_json.get("watchers_count", "-1"),
        forks_count=repo_response_json.get("forks_count", "-1"),
    )
    logger.debug("  received repo: %s", repo)
    return repo


async def _get_last_page_number(paginated_response: ClientResponse) -> int:
    links = paginated_response.links
    try:
        # Making the linters happy in this case just makes the code harder to read
        last_page = links.get("last").get("url").query.get("page")  # type: ignore
        if last_page:
            return int(last_page)
    except AttributeError as some_error:
        logger.debug("Unproblematic error trying to find last page of pull request for count: %s", some_error)
    return 0


async def _get_pull_request_count(uri: str, session: ClientSession, state: Literal["open", "all"]) -> int:
    logger.debug("  fetching pull request count for: %s (%s)", uri, state)
    params = {"per_page": 1, "state": state}
    async with session.get(f"/repos/{uri}/pulls", params=params) as pulls_response:
        return await _get_last_page_number(pulls_response)


async def _get_tag(uri: str, tag_sha: str, sem: asyncio.Semaphore, session: ClientSession) -> Release:
    async with sem:
        async with session.get(f"/repos/{uri}/git/tags/{tag_sha}") as tag_response:
            tag_json = await tag_response.json()
            return Release(tag=tag_json["tag"], created_at=tag_json["tagger"]["date"])


async def _get_releases(uri: str, session: ClientSession) -> List[Release]:
    logger.debug("  fetching releases for: %s", uri)

    tasks = []
    async with session.get(f"/repos/{uri}/git/matching-refs/tags") as tags_response:
        tags_json = await tags_response.json()
        logger.debug("  received %s tags", len(tags_json))

        sem = asyncio.Semaphore(10)
        for tag in tags_json:
            sha = tag["object"]["sha"]
            tasks.append(_get_tag(uri, sha, sem, session))

    releases = await asyncio.gather(*tasks, return_exceptions=False)
    # Sorts releases (aka tags) by date, puts most recent release first
    releases.sort(key=lambda r: _github_datestring_to_datetime(r.created_at), reverse=True)

    return releases


async def _get_commit_count(uri: str, session: ClientSession, since: datetime) -> int:
    logger.debug("  fetching commit count for: %s (since %s)", uri, datetime)
    params = {"per_page": 1, "since": _github_datetime_to_datestring(since)}
    async with session.get(f"/repos/{uri}/commits", params=params) as pulls_response:
        return await _get_last_page_number(pulls_response)


async def _extract_commit_list(response: ClientResponse) -> List[Commit]:
    commit_list_json = await response.json()
    commit_list: List[Commit] = []
    for commit_json in commit_list_json:
        commit_list.append(
            Commit(
                author=Author(
                    name=commit_json.get("commit", {}).get("author", {}).get("name", "unknown"),
                    date=commit_json.get("commit", {}).get("author", {}).get("date", "1970-01-01T00:00:00Z"),
                ),
                message=commit_json.get("commit", {}).get("message", "unknown"),
                comment_count=commit_json.get("commit", {}).get("comment_count", 0),
            )
        )
    return commit_list


async def _get_page_of_commits(url: URL, session: ClientSession, lock_rate: asyncio.Lock, lock_concurrent: asyncio.Semaphore) -> List[Commit]:
    async with lock_concurrent:
        async with lock_rate:
            await asyncio.sleep(0.1)
        logger.debug("  --> fetching commit page at url: %s", url)
        async with session.get(f"{url.path}?{url.query_string}") as commit_response:
            return await _extract_commit_list(commit_response)


async def _generate_urls(next_url: URL, last_url: URL) -> List[URL]:
    logger.debug("  --> generating list of commit URLs")
    next_page_str = next_url.query.get("page")
    last_page_str = last_url.query.get("page")
    first_page = int(next_page_str if next_page_str else "2")
    last_page = int(last_page_str if last_page_str else "2")
    logger.debug("  --> commit URL pages from %s to %s", first_page, last_page)
    urls: List[URL] = []

    for page_number in range(first_page, last_page + 1):
        new_page = URL(next_url)
        query_params = MultiDict(new_page.query)
        query_params.pop("page")
        query_params.add("page", str(page_number))
        new_page = new_page.update_query(query_params)
        urls.append(new_page)

    return urls


async def _get_commits(uri: str, session: ClientSession, since: datetime) -> List[Commit]:
    logger.debug("  getting commits for this repo")
    params = {"per_page": 100, "since": _github_datetime_to_datestring(since)}
    async with session.get(f"/repos/{uri}/commits", params=params) as first_page:
        commit_list = await _extract_commit_list(first_page)
        logger.debug("  --> got the first page of commits")
        next_page = first_page.links.get("next")
        last_page = first_page.links.get("last")
        if next_page and last_page:
            next_url = next_page.get("url")
            last_url = last_page.get("url")

            if next_url and last_url:
                lock_rate = asyncio.Lock()
                lock_concurrent = asyncio.Semaphore(10)

                urls = await _generate_urls(URL(next_url), URL(last_url))
                tasks = [_get_page_of_commits(url, session, lock_rate, lock_concurrent) for url in urls]
                response_list = await asyncio.gather(*tasks)
                commit_list += [commit for commit_list in response_list for commit in commit_list]

        return commit_list


async def _process_commit_data(commits: List[Commit]) -> TimeData:
    logger.info("Getting commit data from APIs")
    deltas: List[float] = []
    previous_date = None
    commit_count = 0
    commits_by_author: Dict[str, int] = {}
    popular_author_count = 0

    for commit in commits:
        commit_count += 1
        commit_author = commit.author
        logger.debug("  author: %s", commit_author.name)
        commits_this_author = commits_by_author.get(commit_author.name, 0) + 1
        commits_by_author[commit_author.name] = commits_this_author
        logger.debug("  commits so far: %s", commits_this_author)

        if commits_this_author > popular_author_count:
            popular_author_count = commits_this_author

        commit_date = _github_datestring_to_datetime(commit_author.date)
        logger.debug("  commit date: %s", commit_date)
        if previous_date is None:
            previous_date = commit_date
            continue

        deltas.append((previous_date - commit_date).total_seconds())
        previous_date = commit_date

    if deltas:
        commit_stats = get_statistics(deltas)
    else:
        commit_stats = Statistics(mean=0, standard_deviation=0)

    return TimeData(
        commit_count=commit_count,
        commit_count_primary_author=popular_author_count,
        commit_interval=commit_stats,
        author_count=len(commits_by_author),
    )


async def _get_days_since_last_commit(commit: Commit) -> int:
    logger.info("  getting days since last commit")
    latest_commit = _github_datestring_to_datetime(commit.author.date)
    since_last_commit = datetime.now().astimezone() - latest_commit
    return since_last_commit.days


async def _get_days_since_last_release(release: Release) -> int:
    logger.info("  getting days since last release")
    latest_release = _github_datestring_to_datetime(release.created_at)
    since_last_release = datetime.now().astimezone() - latest_release
    return since_last_release.days


async def fetch_github_api_data(repo_request_data: RepoRequest) -> DataFromAPI:
    logger.debug("  fetching data from github for: %s", repo_request_data)

    today = datetime.today()
    six_months_ago = datetime.today() - timedelta(days=RECENT_DAYS)

    repo_uri = f"{repo_request_data.owner}/{repo_request_data.repo}"

    headers = {}
    if repo_request_data.sso_token:
        headers["Authorization"] = f"Bearer {repo_request_data.sso_token}"

    async with aiohttp.ClientSession(base_url=BASE_URL, headers=headers, raise_for_status=True) as session:
        repo_http = await _get_repo(repo_uri, session)

        open_pulls = await _get_pull_request_count(repo_uri, session, "open")
        all_pulls = await _get_pull_request_count(repo_uri, session, "all")

        # Paginated API calls for recent commits of git/git: 22
        # Paginated API calls for all commits of git/git: 663
        recent_commits = await _get_commits(repo_uri, session, six_months_ago)

        releases = await _get_releases(repo_uri, session)

    recent_commits.sort(key=lambda c: c.author.date, reverse=True)

    time_data_recent = await _process_commit_data(recent_commits)

    updated_delta = today.date() - _github_datestring_to_datetime(repo_http.updated_at).date()
    days_since_update = updated_delta.days

    created_delta = today.date() - _github_datestring_to_datetime(repo_http.created_at).date()
    days_since_create = created_delta.days

    try:
        days_since_last_commit = await _get_days_since_last_commit(recent_commits[0])
    except IndexError:
        days_since_last_commit = RECENT_DAYS + 1

    try:
        latest_release = releases[0].tag
    except IndexError:
        latest_release = "Unreleased"

    try:
        days_since_last_release = await _get_days_since_last_release(releases[0])
    except IndexError:
        days_since_last_release = None

    return DataFromAPI(
        days_since_update=days_since_update,
        days_since_create=days_since_create,
        watcher_count=repo_http.watchers_count,
        pull_request_count_open=open_pulls,
        pull_request_count=all_pulls,
        open_issue_count=repo_http.open_issues_count,
        days_since_commit=days_since_last_commit,
        time_recent=time_data_recent,
        latest_release=latest_release,
        releases_count=len(releases),
        days_since_last_release=days_since_last_release,
    )
