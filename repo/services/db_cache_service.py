import logging
from datetime import datetime, timedelta

from packaging.version import parse as parse_version
from django.core.exceptions import ObjectDoesNotExist

from repo.data.general import Statistics, RepoRequest
from repo.data.git_data import (
    GitData,
    CommitData,
    PullRequestData,
    CodeData,
    ContributorData,
    PopularityData,
)
from repo.models import CacheData
from repo.services.errors import CacheMiss

logger = logging.getLogger(__name__)

RECENT_DAYS = 30


def check_cache(current_version: str, url_metadata: RepoRequest) -> GitData:
    logger.debug("Checking cache for existing data: %s", url_metadata)

    try:
        found: CacheData = CacheData.objects.get_by_natural_key(
            source=url_metadata.source, owner=url_metadata.owner, repo=url_metadata.repo
        )
    except ObjectDoesNotExist as object_does_not_exist:
        raise CacheMiss() from object_does_not_exist
    logger.info("Found cached data for: %s", url_metadata)

    recent = datetime.today() - timedelta(days=RECENT_DAYS)
    logger.debug("type for found.row_updated_date: %s", type(found.row_updated_date))
    logger.debug("type for recent: %s", type(recent))
    if found.row_updated_date < recent.date():
        raise CacheMiss()

    current_version_parsed = parse_version(current_version)
    found_version_parsed = parse_version(found.version)
    if current_version_parsed > found_version_parsed:
        raise CacheMiss()

    return GitData(
        code=CodeData(
            lines_of_code=found.code_lines_of_code,
            file_count=found.code_file_count,
        ),
        pull_request=PullRequestData(
            count_open=found.pull_request_count_open,
            count=found.pull_request_count,
        ),
        commit_all=CommitData(
            count=found.commit_all_count,
            count_primary_author=found.commit_all_count_primary_author,
            interval=Statistics(
                mean=found.commit_all_interval_mean,
                standard_deviation=found.commit_all_interval_standard_deviation,
            ),
        ),
        commit_recent=CommitData(
            count=found.commit_recent_count,
            count_primary_author=found.commit_recent_count_primary_author,
            interval=Statistics(
                mean=found.commit_recent_interval_mean,
                standard_deviation=found.commit_recent_interval_standard_deviation,
            ),
        ),
        contributor=ContributorData(
            days_since_create=found.contributor_days_since_create,
            days_since_commit=found.contributor_days_since_commit,
            branch_count=found.contributor_branch_count,
            author_count_all=found.contributor_author_count_all,
            author_count_recent=found.contributor_author_count_recent,
        ),
        popularity=PopularityData(
            watcher_count=found.popularity_watcher_count,
            has_issues=found.popularity_has_issues,
            open_issue_count=found.popularity_open_issue_count,
        ),
    )


def patch_cache(
    version: str,
    url_metadata: RepoRequest,
    data: GitData,
) -> None:
    logger.debug("Updating cached data for: %s", url_metadata)
    logger.debug("  data: %s", data)

    try:
        found: CacheData = CacheData.objects.get_by_natural_key(
            source=url_metadata.source, owner=url_metadata.owner, repo=url_metadata.repo
        )
        found.version = version

        # UrlMetadata + Primary Key
        found.source = url_metadata.source
        found.owner = url_metadata.owner
        found.repo = url_metadata.repo

        # Data
        found.code_lines_of_code = data.code.lines_of_code
        found.code_file_count = data.code.file_count

        found.pull_request_count_open = data.pull_request.count_open
        found.pull_request_count = data.pull_request.count

        found.commit_all_count = data.commit_all.count
        found.commit_all_count_primary_author = data.commit_all.count_primary_author
        found.commit_all_interval_mean = data.commit_all.interval.mean
        found.commit_all_interval_standard_deviation = (
            data.commit_all.interval.standard_deviation
        )

        found.commit_recent_count = data.commit_recent.count
        found.commit_recent_count_primary_author = (
            data.commit_recent.count_primary_author
        )
        found.commit_recent_interval_mean = data.commit_recent.interval.mean
        found.commit_recent_interval_standard_deviation = (
            data.commit_recent.interval.standard_deviation
        )

        found.contributor_days_since_create = data.contributor.days_since_create
        found.contributor_days_since_commit = data.contributor.days_since_commit
        found.contributor_branch_count = data.contributor.branch_count
        found.contributor_author_count_all = data.contributor.author_count_all
        found.contributor_author_count_recent = data.contributor.author_count_recent

        found.popularity_watcher_count = data.popularity.watcher_count
        found.popularity_has_issues = data.popularity.has_issues
        found.popularity_open_issue_count = data.popularity.open_issue_count

        found.save()
    except ObjectDoesNotExist:
        git_repo_data = CacheData.objects.create_git_repo_data(
            version=version, url_metadata=url_metadata, data=data
        )
        git_repo_data.save()
