# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,

import pytest

from repo.models import GitRepoData
from repo.services.data import UrlMetadata, ApiData, LocalData
from repo.services.db_cache_service import patch_cache, check_cache


@pytest.fixture
def fake_url_metadata():
    return UrlMetadata(source="test-source", owner="test-owner", repo="test-repo")


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
        lines_of_code_total=-1,
        files_total=-1,
    )


@pytest.mark.django_db
def test_cache(fake_url_metadata, fake_api_data, fake_local_data):
    with pytest.raises(GitRepoData.DoesNotExist):
        check_cache(fake_url_metadata)

    patch_cache(fake_url_metadata, fake_api_data, fake_local_data)
    found = check_cache(fake_url_metadata)
    assert found
