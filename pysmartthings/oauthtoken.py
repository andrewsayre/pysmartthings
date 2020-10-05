"""Define the oauth module."""

from datetime import datetime, timedelta
from typing import List, Optional

from .api import Api


class OAuthToken:
    """Define oauth token information."""

    def __init__(
        self, api: Api, data: Optional[dict] = None, refresh_token: Optional[str] = None
    ):
        """Create a new instance of the OAuthToken class."""
        self._api = api
        self._access_token = None
        self._refresh_token = refresh_token
        self._expires_in = 0
        self._token_type = None
        self._scope = []
        self._expiration_date = datetime.now()
        if data:
            self.apply_data(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        self._access_token = data["access_token"]
        self._token_type = data["token_type"]
        self._refresh_token = data["refresh_token"]
        self._expires_in = data["expires_in"]
        self._expiration_date = datetime.now() + timedelta(0, self._expires_in)
        data_scope = data["scope"]
        if isinstance(data_scope, list):
            self._scope = data_scope
        if isinstance(data_scope, str):
            self._scope.clear()
            self._scope.append(data_scope)

    async def refresh(self, client_id: str, client_secret: str):
        """Refresh the auth and refresh tokens."""
        data = await self._api.generate_tokens(
            client_id, client_secret, self._refresh_token
        )
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

    @property
    def expiration_date(self) -> datetime:
        """Get the date when the token expires."""
        return self._expiration_date

    @property
    def is_expired(self):
        """Return True if the token has expired."""
        return datetime.now() > self._expiration_date
