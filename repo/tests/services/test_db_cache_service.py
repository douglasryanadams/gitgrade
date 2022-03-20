# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest
from freezegun import freeze_time

from repo.data.general import Statistics
from repo.data.git_data import (
    GitData,
    PullRequestData,
    CommitData,
    ContributorData,
    PopularityData,
)
from repo.services.db_cache_service import patch_cache, check_cache
from repo.services.errors import CacheMiss
from repo.services.repo_input_service import RepoRequest


@pytest.fixture
def fake_url_metadata():
    return RepoRequest(source="test-source", owner="test-owner", repo="test-repo")


@pytest.fixture
def fake_git_data():
    return GitData(
        # code=CodeData(
        #     lines_of_code=-1,
        #     file_count=-1,
        # ),
        pull_request=PullRequestData(
            count_open=-1,
            count=-1,
        ),
        # commit_all=CommitData(
        #     count=-1,
        #     count_primary_author=-1,
        #     interval=Statistics(
        #         mean=-1,
        #         standard_deviation=-1,
        #     ),
        # ),
        commit_recent=CommitData(
            count=-1,
            count_primary_author=-1,
            interval=Statistics(
                mean=-1,
                standard_deviation=-1,
            ),
        ),
        contributor=ContributorData(
            days_since_create=-1,
            days_since_commit=-1,
            branch_count=-1,
            # author_count_all=-1,
            author_count_recent=-1,
        ),
        popularity=PopularityData(
            watcher_count=-1, has_issues=False, open_issue_count=-1
        ),
    )


@pytest.mark.django_db
def test_cache(fake_url_metadata, fake_git_data):
    with pytest.raises(CacheMiss):
        check_cache("0.0.0", fake_url_metadata)

    patch_cache("0.0.0", fake_url_metadata, fake_git_data)
    found = check_cache("0.0.0", fake_url_metadata)
    assert found


@pytest.mark.django_db
def test_cache_expired_update(fake_url_metadata, fake_git_data):
    patch_cache("0.0.0", fake_url_metadata, fake_git_data)

    with freeze_time("2100-01-01"):  # Date in the far future, I would have been 114
        with pytest.raises(CacheMiss):
            check_cache("0.0.0", fake_url_metadata)

    fake_git_data.contributor.days_since_create = 10
    patch_cache("0.0.0", fake_url_metadata, fake_git_data)
    found = check_cache("0.0.0", fake_url_metadata)
    assert found
    assert found.contributor.days_since_create == 10


@pytest.mark.django_db
def test_cache_old_version_update(fake_url_metadata, fake_git_data):
    patch_cache("0.0.0", fake_url_metadata, fake_git_data)

    with pytest.raises(CacheMiss):
        check_cache("0.0.1", fake_url_metadata)

    patch_cache("0.0.1", fake_url_metadata, fake_git_data)
    found = check_cache("0.0.1", fake_url_metadata)
    assert found
