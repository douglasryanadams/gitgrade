import logging
from dataclasses import dataclass
from urllib.parse import urlparse

from django.core.validators import URLValidator

logger = logging.getLogger(__name__)

validate_url = URLValidator()
hostname_to_source = {
    "github.com": "github",
    "bitbucket.org": "bitbucket",
}


def _get_github_name(path: str) -> str:
    logger.debug("parsing github path: %s", path)
    return path.split("/")[2]


def _get_bitbucket_name(path: str) -> str:
    logger.debug("parsing bitbucket path: %s", path)
    return path.split("/")[2]


path_to_repo_name = {"github": _get_github_name, "bitbucket": _get_bitbucket_name}


@dataclass
class SourceMetadata:
    source_name: str
    repo_name: str


class UnsupportedURL(Exception):
    ...


def identify_source(repo_url: str) -> SourceMetadata:
    """
    This method returns metadata about the repo based on the URL

    :param repo_url: URL of the repo we want to grade
    :return SourceMetadata: Object containing metadata we can extract from the URL
    """
    logger.info("Identifying source of: %s", repo_url)
    validate_url(repo_url)

    parsed_url = urlparse(repo_url)
    hostname = parsed_url.hostname
    if hostname:
        source_name = hostname_to_source.get(hostname)
    else:
        raise UnsupportedURL(f"{repo_url} does not contain a valid hostname")

    if not source_name:
        raise UnsupportedURL(f"{repo_url} is not currently supported")

    path = parsed_url.path
    repo_name = path_to_repo_name[source_name](path)

    return SourceMetadata(source_name=source_name, repo_name=repo_name)
