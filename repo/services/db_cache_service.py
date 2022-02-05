import logging
from datetime import datetime, timedelta
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist

from repo.models import GitRepoData
from repo.services.data import LocalData, ApiData, RepoRequestData
from repo.services.errors import CacheMiss

logger = logging.getLogger(__name__)

RECENT_DAYS = 30


def check_cache(url_metadata: RepoRequestData) -> Tuple[ApiData, LocalData]:
    logger.debug("Checking cache for existing data: %s", url_metadata)

    try:
        found: GitRepoData = GitRepoData.objects.get_by_natural_key(
            source=url_metadata.source, owner=url_metadata.owner, repo=url_metadata.repo
        )
    except ObjectDoesNotExist as odne:
        raise CacheMiss() from odne
    logger.info("Found cached data for: %s", url_metadata)

    recent = datetime.today() - timedelta(days=RECENT_DAYS)
    logger.debug("type for found.row_updated_date: %s", type(found.row_updated_date))
    logger.debug("type for recent: %s", type(recent))
    if found.row_updated_date < recent.date():
        raise CacheMiss()

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
    url_metadata: RepoRequestData, api_data: ApiData, local_data: LocalData
) -> None:
    logger.debug("Updating cached data for: %s", url_metadata)
    logger.debug("  api_data: %s", api_data)
    logger.debug("  local_data: %s", local_data)
    try:
        found: GitRepoData = GitRepoData.objects.get_by_natural_key(
            source=url_metadata.source, owner=url_metadata.owner, repo=url_metadata.repo
        )

        found.days_since_update = api_data.days_since_update
        found.days_since_create = api_data.days_since_create
        found.watchers = api_data.watchers
        found.pull_requests_open = api_data.pull_requests_open
        found.pull_requests_total = api_data.pull_requests_total
        found.has_issues = api_data.has_issues
        found.open_issues = api_data.open_issues
        found.days_since_commit = local_data.days_since_commit
        found.commits_total = local_data.commits_total
        found.commits_recent = local_data.commits_recent
        found.branch_count = local_data.branch_count
        found.authors_total = local_data.authors_total
        found.authors_recent = local_data.authors_recent
        found.prolific_author_commits_total = local_data.prolific_author_commits_total
        found.prolific_author_commits_recent = local_data.prolific_author_commits_recent
        found.lines_of_code_total = local_data.lines_of_code_total
        found.files_total = local_data.files_total

        found.save()
    except ObjectDoesNotExist:
        git_repo_data = GitRepoData.objects.create_git_repo_data(
            url_metadata=url_metadata, api_data=api_data, local_data=local_data
        )
        git_repo_data.save()
