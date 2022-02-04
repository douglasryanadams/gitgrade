import logging
from typing import Dict
from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


def github_sso_url(request: HttpRequest) -> Dict[str, str]:
    """
    We want to use Github's SSO for users to a much higher rate limit for Github calls,
    using the OAuth App workflow allows users to get data on the repos they're curious
    about and allows us to collect the data for those repos using the rate limit of the
    users.

    Note: We're not using 'state' yet because we're not using 'scopes' so it feels unnecessary,
    if we add support for 'scopes' that allow access to private user data, add support for
    'state' to defend against CSRF attacks.

    More info: https://auth0.com/docs/secure/attack-protection/state-parameters
    """
    logger.debug("Rendering github_sso_url")

    params = {
        "redirect_uri": f"{settings.GITGRADE_BASE_URL}/authorization/github",
        "client_id": settings.GITHUB_SSO_CLIENT_ID,
        "client_secret": settings.GITHUB_SSO_CLIENT_SECRET,
        # "scopes": []  # Don't handle private data since we cache it, so no scopes
    }
    logger.debug("  Github SSO params: %s", params)
    param_string = urlencode(params)

    base_url = "https://github.com/login/oauth/authorize"
    return {"GITHUB_SSO_URL": f"{base_url}?{param_string}"}
