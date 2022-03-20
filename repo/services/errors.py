class UnsupportedURL(Exception):
    """
    A URL was provided for a git repo that's not supported
    """

    ...


class ClocMissingError(Exception):
    """
    Cloc utility is not installed
    """

    ...


class CacheMiss(Exception):
    """
    Tried to pull data from the cache, but it's not in their or its out of date
    """

    ...


class InvalidRequest(Exception):
    """
    Something about the request was invalid but there's something the user can do to fix it
    """

    ...
