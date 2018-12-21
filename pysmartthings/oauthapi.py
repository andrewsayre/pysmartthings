"""Define the OAuthAPI module."""

import requests

from .errors import APIInvalidGrant, APIUnauthorizedError, APIUnknownError

AUTH_API_TOKEN = "https://auth-global.api.smartthings.com/oauth/token"


class OAuthAPI:
    """Define the OAuthAPI class."""

    def __init__(self, client_id: str, client_secret: str):
        """Initialize a new instance of the OAuthAPI."""
        self._client_id = client_id
        self._client_secret = client_secret

    def get_token(self, refresh_token: str):
        """Obtain a new access and refresh token."""
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        resp = requests.post(AUTH_API_TOKEN,
                             auth=(self._client_id, self._client_secret),
                             data=payload)
        if resp.ok:
            return resp.json()
        if resp.status_code == 400:
            data = resp.json()
            raise APIInvalidGrant(data['error_description'])
        if resp.status_code == 401:
            raise APIUnauthorizedError
        raise APIUnknownError
