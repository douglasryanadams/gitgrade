# pylint: disable=redefined-outer-name, unused-argument, missing-function-docstring,
from typing import Union

import pytest
from django.core.exceptions import ValidationError

from repo.data.general import RepoRequest
from repo.services.errors import UnsupportedURL
from repo.services.url_service import identify_source


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/git/git",
            RepoRequest(source="github", owner="git", repo="git"),
        ),
        (
            "https://github.com/apache/httpd",
            RepoRequest(source="github", owner="apache", repo="httpd"),
        ),
        (
            "https://bitbucket.org/atlassian/bamboo-tomcat-plugin/src/master/",
            RepoRequest(source="bitbucket", owner="atlassian", repo="bamboo-tomcat-plugin"),
        ),
        (
            "https://bitbucket.org/schae/test-test-test/src/master/",
            RepoRequest(source="bitbucket", owner="schae", repo="test-test-test"),
        ),
        (
            "https://opensource.ncsa.illinois.edu/bitbucket/projects/ERGO/repos/tutorial/browse",
            UnsupportedURL,
        ),
        ("https://www.google.com/", UnsupportedURL),
        ("gobbledygook", ValidationError),
    ],
)
def test_identify_source(url: str, expected: Union[RepoRequest, BaseException]) -> None:
    """
    Should make sure we're parsing repo paths correctly and document our supported/unsupported URL examples
    """
    if isinstance(expected, RepoRequest):
        actual_metadata = identify_source(url)
        assert actual_metadata == expected
    else:
        with pytest.raises(expected):  # type: ignore
            identify_source(url)
