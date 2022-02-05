# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest
from freezegun import freeze_time

from repo.services.data import RepoRequestData, ApiData, LocalData
from repo.services.db_cache_service import patch_cache, check_cache
from repo.services.errors import CacheMiss


@pytest.fixture
def fake_url_metadata():
    return RepoRequestData(source="test-source", owner="test-owner", repo="test-repo")


@pytest.fixture
def fake_api_data():
    return ApiData(
        days_since_update=-1,
        days_since_create=-1,
        watchers=-1,
        pull_requests_open=-1,
        pull_requests_total=-1,
        has_issues=False,
        open_issues=-1,
    )


@pytest.fixture
def fake_local_data():
    return LocalData(
        days_since_commit=-1,
        commits_total=-1,
        commits_recent=-1,
        branch_count=-1,
        authors_total=-1,
        authors_recent=-1,
        prolific_author_commits_total=-1,
        prolific_author_commits_recent=-1,
        lines_of_code_total=-1,
        files_total=-1,
    )


@pytest.mark.django_db
def test_cache(fake_url_metadata, fake_api_data, fake_local_data):
    with pytest.raises(CacheMiss):
        check_cache(fake_url_metadata)

    patch_cache(fake_url_metadata, fake_api_data, fake_local_data)
    found = check_cache(fake_url_metadata)
    assert found


@pytest.mark.django_db
def test_cache_expired_update(fake_url_metadata, fake_api_data, fake_local_data):
    patch_cache(fake_url_metadata, fake_api_data, fake_local_data)

    with freeze_time("2100-01-01"):  # Date in the far future, I would have been 114
        with pytest.raises(CacheMiss):
            check_cache(fake_url_metadata)

    fake_api_data.days_since_create = 10
    patch_cache(fake_url_metadata, fake_api_data, fake_local_data)
    found = check_cache(fake_url_metadata)
    assert found
    assert found[0].days_since_create == 10
