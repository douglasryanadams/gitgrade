import logging
from typing import Tuple

from repo.models import GitRepoData
from repo.services.data import LocalData, ApiData, UrlMetadata

logger = logging.getLogger(__name__)


def check_cache(url_metadata: UrlMetadata) -> Tuple[ApiData, LocalData]:
    logger.debug("Checking cache for existing data: %s", url_metadata)

    found: GitRepoData = GitRepoData.objects.get_by_natural_key(
        source=url_metadata.source, owner=url_metadata.owner, repo=url_metadata.repo
    )
    logger.info("Found cached data for: %s", url_metadata)

    api_data = ApiData(
        days_since_update=found.days_since_update,
        days_since_create=found.days_since_create,
        watchers=found.watchers,
        pull_requests_open=found.pull_requests_open,
        pull_requests_total=found.pull_requests_total,
        has_issues=found.has_issues,
        open_issues=found.open_issues,
    )

    local_data = LocalData(
        days_since_commit=found.days_since_commit,
        commits_total=found.commits_total,
        commits_recent=found.commits_recent,
        branch_count=found.branch_count,
        authors_total=found.authors_total,
        authors_recent=found.authors_recent,
        prolific_author_commits_total=found.prolific_author_commits_total,
        prolific_author_commits_recent=found.prolific_author_commits_recent,
        lines_of_code_total=found.lines_of_code_total,
        files_total=found.files_total,
    )

    return api_data, local_data


def patch_cache(
    url_metadata: UrlMetadata, api_data: ApiData, local_data: LocalData
) -> None:
    logger.debug("Updating cached data for: %s", url_metadata)
    logger.debug("  api_data: %s", api_data)
    logger.debug("  local_data: %s", local_data)
    git_repo_data = GitRepoData.objects.create_git_repo_data(
        url_metadata=url_metadata, api_data=api_data, local_data=local_data
    )
    git_repo_data.save()
