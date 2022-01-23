import logging
from urllib.parse import urlparse

from django.core.validators import URLValidator

from repo.services.data import UrlMetadata
from repo.services.errors import UnsupportedURL

hostname_to_source = {
    "github.com": "github",
    "bitbucket.org": "bitbucket",
}

logger = logging.getLogger(__name__)


def identify_source(repo_url: str) -> UrlMetadata:
    """
    This method returns metadata about the repo based on the URL

    :param repo_url: URL of the repo we want to grade
    :return SourceMetadata: Object containing metadata we can extract from the URL
    """
    logger.info("Identifying source of: %s", repo_url)

    validate_url = URLValidator()
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
    path_parts = path.split("/")

    # If we add support for something that doesn't match this pattern, we should refactor
    owner_name = path_parts[1]
    repo_name = path_parts[2]

    logger.debug("  source: %s", source_name)
    logger.debug("  owner: %s", owner_name)
    logger.debug("  repo: %s", repo_name)
    return UrlMetadata(source=source_name, owner=owner_name, repo=repo_name)
