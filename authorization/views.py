# Create your views here.
import logging

import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

logger = logging.getLogger(__name__)


def github_authorization(request: HttpRequest) -> HttpResponse:
    """
    Handles the callbacks from Github as part of the OAuth handshake
    """
    logger.info("Received Github callback")
    code: str = request.GET.get("code", "missing_code")
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.GITHUB_SSO_CLIENT_ID,
            "client_secret": settings.GITHUB_SSO_CLIENT_SECRET,
            "code": code,
            "redirect_uri": f"{settings.GITGRADE_BASE_URL}/authorization/github"
        },
        headers={
            "Accept": "application/json"
        }
    )
    logger.debug('  response from github: %s', response)

    json_response = response.json()
    logger.debug('  json_response: %s', json_response)

    send_home = redirect('/')
    send_home.set_cookie(
        'github_token',
        value=json_response['access_token'],
        max_age=24 * 60 * 60,  # age in seconds
        path='/'
    )

    return send_home
