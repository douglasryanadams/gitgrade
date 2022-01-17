from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    """
    Custom Constants
    """

    GITHUB_API_URL = "https://api.github.com"
    BITBUCKET_API_URL = "https://api.bitbucket.org/2.0"
    BITBUCKET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
