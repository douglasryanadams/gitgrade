from typing import Union

import pytest
from django.core.exceptions import ValidationError

from repo.services import SourceMetadata, identify_source, UnsupportedURL


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/git/git",
            SourceMetadata(source_name="github", repo_name="git"),
        ),
        (
            "https://github.com/apache/httpd",
            SourceMetadata(source_name="github", repo_name="httpd"),
        ),
        (
            "https://bitbucket.org/atlassian/bamboo-tomcat-plugin/src/master/",
            SourceMetadata(source_name="bitbucket", repo_name="bamboo-tomcat-plugin"),
        ),
        (
            "https://bitbucket.org/schae/test-test-test/src/master/",
            SourceMetadata(source_name="bitbucket", repo_name="test-test-test"),
        ),
        (
            "https://opensource.ncsa.illinois.edu/bitbucket/projects/ERGO/repos/tutorial/browse",
            UnsupportedURL,
        ),
        ("https://www.google.com/", UnsupportedURL),
        ("gobbledygook", ValidationError),
    ],
)
def test_identify_source(
    url: str, expected: Union[SourceMetadata, BaseException]
) -> None:
    """
    Should make sure we're parsing repo paths correctly and document our supported/unsupported URL examples
    """
    if isinstance(expected, SourceMetadata):
        actual_metadata = identify_source(url)
        assert actual_metadata == expected
    else:
        with pytest.raises(expected):  # type: ignore
            identify_source(url)
