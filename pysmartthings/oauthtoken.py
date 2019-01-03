"""Define the oauth module."""

from typing import List, Optional

from .api import Api


class OAuthToken:
    """Define oauth token information."""

    def __init__(self, api: Api, data: Optional[dict] = None,
                 refresh_token: Optional[str] = None):
        """Create a new instance of the OAuthToken class."""
        self._api = api
        self._access_token = None
        self._refresh_token = refresh_token
        self._expires_in = 0
        self._token_type = None
        self._scope = []
        if data:
            self.apply_data(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        self._access_token = data['access_token']
        self._token_type = data['token_type']
        self._refresh_token = data['refresh_token']
        self._expires_in = data['expires_in']
        data_scope = data['scope']
        if isinstance(data_scope, list):
            self._scope = data_scope
        if isinstance(data_scope, str):
            self._scope.clear()
            self._scope.append(data_scope)

    async def refresh(self, client_id: str, client_secret: str):
        """Refresh the auth and refresh tokens."""
        data = await self._api.get_token(self._refresh_token, client_id,
                                         client_secret)
        if data:
            self.apply_data(data)

    @property
    def access_token(self) -> str:
        """Get the access token for authentication."""
        return self._access_token

    @property
    def refresh_token(self) -> str:
        """Get the refresh token for obtaining new access tokens."""
        return self._refresh_token

    @property
    def expires_in(self) -> int:
        """Get the amount of time in seconds until the token expires."""
        return self._expires_in

    @property
    def token_type(self) -> str:
        """Get the type of token."""
        return self._token_type

    @property
    def scope(self) -> List[str]:
        """Get the scopes the token has permission to."""
        return self._scope
