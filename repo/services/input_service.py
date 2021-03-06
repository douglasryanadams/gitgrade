import logging
from dataclasses import asdict, dataclass
from typing import Optional, Dict, Final, Any, Literal

from aiohttp import ClientResponseError, ClientError
from asgiref.sync import async_to_sync
from django.core.exceptions import ValidationError

from gitgrade.util import get_version
from repo.data.from_source import DataFromAPI
from repo.data.general import RepoRequest, ViewOnly
from repo.data.git_data import (
    GitData,
    PullRequestData,
    CommitData,
    ContributorData,
    PopularityData,
)
from repo.data.grade import TestGrades
from repo.services.db_cache_service import check_cache, patch_cache
from repo.services.errors import CacheMiss, UnsupportedURL
from repo.services.grade_calculator_service import calculate_grade
from repo.services.rest_api_service_async import (
    fetch_github_api_data as fetch_github_api_data_async,
)
from repo.services.url_service import identify_source

logger = logging.getLogger(__name__)


@dataclass
class RepoResult:
    """
    This class represents the response objected use in the
    result view.
    """

    status: Literal["success"]
    request: RepoRequest
    grades: TestGrades
    data: GitData
    view: ViewOnly


@dataclass
class ErrorResult:
    status: Literal["error"]
    error_message: str


# def _convert(api_data: DataFromAPI, clone_data: DataFromClone) -> GitData:
def _convert(api_data: DataFromAPI) -> GitData:
    return GitData(
        # code=CodeData(
        #     lines_of_code=clone_data.lines_of_code,
        #     file_count=clone_data.file_count,
        # ),
        pull_request=PullRequestData(
            count=api_data.pull_request_count,
            count_open=api_data.pull_request_count_open,
        ),
        # commit_all=CommitData(
        #     count=clone_data.time_all.commit_count,
        #     count_primary_author=clone_data.time_all.commit_count_primary_author,
        #     interval=clone_data.time_all.commit_interval,
        # ),
        commit_recent=CommitData(
            # count=clone_data.time_recent.commit_count,
            # count_primary_author=clone_data.time_recent.commit_count_primary_author,
            # interval=clone_data.time_recent.commit_interval,
            count=api_data.time_recent.commit_count,
            count_primary_author=api_data.time_recent.commit_count_primary_author,
            interval=api_data.time_recent.commit_interval,
        ),
        contributor=ContributorData(
            days_since_create=api_data.days_since_create,
            # days_since_commit=clone_data.days_since_commit,
            # branch_count=clone_data.branch_count,
            # author_count_all=clone_data.time_all.author_count,
            # author_count_recent=clone_data.time_recent.author_count,
            days_since_commit=api_data.days_since_commit,
            author_count_recent=api_data.time_recent.author_count,
        ),
        popularity=PopularityData(
            watcher_count=api_data.watcher_count,
            open_issue_count=api_data.open_issue_count,
        ),
    )


def input_util(  # pylint: disable=too-many-return-statements  # refactor this later
    repo_url: Optional[str] = None,
    source: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
    github_token: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        if repo_url:
            repo_request = identify_source(repo_url)
        elif source and owner and repo:
            repo_request = RepoRequest(source=source, owner=owner, repo=repo)
        else:
            raise UnsupportedURL("Could not figure out source")
    except ValidationError:
        logger.exception("Error parsing request URL")
        return asdict(ErrorResult(status="error", error_message="Please provide a valid Github URL"))
    except UnsupportedURL:
        logger.exception("Unsupported URL received")
        return asdict(ErrorResult(status="error", error_message="URL provided is not supported, please provide a valid Github URL"))

    if repo_request.source != "github":
        return {"status": "error", "error_message": "Please provide a valid Github URL, the URL provided was not from Github."}

    current_version = get_version()

    try:
        git_data = check_cache(current_version, repo_request)
    except CacheMiss:
        repo_request.sso_token = github_token

        fetch_github_api_data = async_to_sync(fetch_github_api_data_async)  # type: ignore
        try:
            api_data = fetch_github_api_data(repo_request)
        except ClientResponseError as client_response_error:

            if client_response_error.status == 403:
                if github_token:
                    return asdict(ErrorResult(status="error", error_message="You've reached the rate limit for Github, please wait a while and try again"))
                return {"status": "error", "error_message": "Please sign in to Github to proceed."}

            if client_response_error.status == 404:
                return asdict(ErrorResult(status="error", error_message="The repo you requested does not exist."))

            logger.exception("Unexpected ClientResponseError while parsing data")
            return asdict(ErrorResult(status="error", error_message="Unexpected error, please retry or create an issue on our github."))

        except ClientError:
            logger.exception("Unexpected ClientError while parsing data")
            return asdict(ErrorResult(status="error", error_message="Unexpected error, please retry or create an issue on our github."))
        # clone_data = fetch_clone_data(repo_request)

        git_data = _convert(api_data)
        patch_cache(current_version, repo_request, git_data)

    test_grades: Final[TestGrades] = calculate_grade(git_data)

    view_only = ViewOnly(
        # commit_interval_days_all=f"{test_grades.commit_interval_all.raw_number:.2f}",
        commit_interval_days_recent=f"{test_grades.commit_interval_recent.raw_number:.2f}",
    )

    result = RepoResult(request=repo_request, grades=test_grades, data=git_data, view=view_only, status="success")
    return asdict(result)
